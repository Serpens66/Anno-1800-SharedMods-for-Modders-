# SPDX-License-Identifier: MIT
[CmdletBinding()]
param([string]$ConfigPath)

$ErrorActionPreference = 'Stop'
# PS 5.1 can evaluate parameter defaults before PSScriptRoot is available.
if ([string]::IsNullOrWhiteSpace($ConfigPath)) {
    $ConfigPath = Join-Path (Split-Path -Parent $PSScriptRoot) 'local.json'
}
$script:Issues = 0
function Report([string]$Level, [string]$Message) {
    Write-Output "[$Level] $Message"
    if ($Level -eq 'ERROR') { $script:Issues++ }
}
function Resolve-LocalPath([string]$Value, [string]$Base) {
    if ([string]::IsNullOrWhiteSpace($Value)) { return '' }
    if ([IO.Path]::IsPathRooted($Value)) { return [IO.Path]::GetFullPath($Value) }
    return [IO.Path]::GetFullPath((Join-Path $Base $Value))
}
function Is-Inside([string]$Child, [string]$Parent) {
    $prefix = $Parent.TrimEnd([char[]]'\/') + [IO.Path]::DirectorySeparatorChar
    return $Child.Equals($Parent, [StringComparison]::OrdinalIgnoreCase) -or $Child.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)
}
function Has-String($Object, [string]$Key) {
    $property = $Object.PSObject.Properties[$Key]
    return $null -ne $property -and $property.Value -is [string]
}

try {
    $fullConfig = [IO.Path]::GetFullPath($ConfigPath)
    if (-not (Test-Path -LiteralPath $fullConfig -PathType Leaf)) {
        Report 'ERROR' 'Local configuration is missing. Copy local.example.json to local.json and follow setup.md.'
        exit 1
    }
    $base = Split-Path -Parent $fullConfig
    try {
        $raw = Get-Content -LiteralPath $fullConfig -Raw -Encoding UTF8
        # Newer ConvertFrom-Json accepts JSONC. Reject comments/trailing commas
        # outside strings to keep the same strict-JSON contract on PS 5.1 and 7.
        $outsideStrings = [regex]::Replace($raw, '"(?:[^"\\]|\\.)*"', '""')
        if ($outsideStrings -match '//|/\*|,\s*[}\]]') { throw 'Strict JSON required.' }
        $config = $raw | ConvertFrom-Json
    } catch { Report 'ERROR' 'Configuration is not strict JSON. Check comments, commas, quotes and escaped backslashes.'; exit 1 }
    if ($null -eq $config -or $config -isnot [PSCustomObject]) { Report 'ERROR' 'Configuration must be a JSON object.'; exit 1 }
    if ($config.configVersion -isnot [ValueType] -or $config.configVersion -is [bool] -or $config.configVersion -ne 1) {
        Report 'ERROR' 'configVersion must be the number 1.'
    }
    $paths = @{}
    foreach ($key in @('gamePath','vanillaPath','modsPath','workPath','outputPath')) {
        if (-not (Has-String $config $key)) { Report 'ERROR' "$key must be a JSON string."; continue }
        if ($key -ne 'modsPath' -and [string]::IsNullOrWhiteSpace($config.$key)) {
            Report 'ERROR' "$key is empty; set it in local.json."; continue
        }
        $paths[$key] = Resolve-LocalPath $config.$key $base
    }
    if ($script:Issues -gt 0) { exit 1 }
    # Optional research roots are not prerequisites for ordinary mod work.
    $sourcePaths = @()
    foreach ($key in @('workspacePath','researchPath')) {
        if ($config.PSObject.Properties.Name -contains $key) {
            if (-not (Has-String $config $key)) { Report 'ERROR' "$key must be a JSON string."; continue }
            $sourceRoot = Resolve-LocalPath $config.$key $base
            if ($sourceRoot) {
                $sourcePaths += $sourceRoot
                if (-not (Test-Path -LiteralPath $sourceRoot -PathType Container)) { Report 'WARN' "$key is unavailable; related research scans cannot run." }
            }
        }
    }
    foreach ($key in @('sources','pathAliases')) {
        if ($config.PSObject.Properties.Name -notcontains $key) { continue }
        if ($config.$key -isnot [PSCustomObject]) { Report 'ERROR' "$key must map names to path strings."; continue }
        foreach ($entry in $config.$key.PSObject.Properties) {
            if ($entry.Value -isnot [string]) { Report 'ERROR' "$key entries must be JSON strings."; continue }
            if ([string]::IsNullOrWhiteSpace($entry.Value)) { continue }
            $sourceRoot = Resolve-LocalPath $entry.Value $base
            $sourcePaths += $sourceRoot
            if (-not (Test-Path -LiteralPath $sourceRoot)) { Report 'WARN' "$key source is unavailable: $($entry.Name)." }
        }
    }
    $documentationRoot = Split-Path -Parent $PSScriptRoot
    foreach ($key in @('workPath','outputPath')) {
        $folderName = if ($key -eq 'workPath') { 'work' } else { 'out' }
        $allowedDefault = Join-Path $documentationRoot $folderName
        if ($paths[$key].Equals($allowedDefault, [StringComparison]::OrdinalIgnoreCase)) { continue }
        foreach ($sourceRoot in @($documentationRoot) + $sourcePaths) {
            if ((Is-Inside $paths[$key] $sourceRoot) -or (Is-Inside $sourceRoot $paths[$key])) {
                Report 'ERROR' "$key overlaps a maintained/source directory; choose separate work/output locations."
            }
        }
    }
    if ($script:Issues -gt 0) { exit 1 }
    if (-not (Test-Path -LiteralPath (Join-Path $paths.gamePath 'Bin/Win64/Anno1800.exe') -PathType Leaf)) {
        Report 'ERROR' 'gamePath does not contain Bin/Win64/Anno1800.exe. Select the installation root.'
    } else { Report 'OK' 'Anno 1800 executable is present (presence only; build not verified).' }
    foreach ($name in @('assets.xml','templates.xml','properties-toolone.xml','properties.xml','datasets.xml')) {
        $file = Join-Path $paths.vanillaPath ('data/config/export/main/asset/' + $name)
        if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { Report 'ERROR' "Missing vanilla $name; extract current game data into a separate directory." }
        elseif ((Get-Item -LiteralPath $file).Length -eq 0) { Report 'ERROR' "Vanilla $name is empty." }
        else { Report 'OK' "Vanilla $name is present (freshness/content not verified)." }
    }
    foreach ($key in @('workPath','outputPath')) {
        foreach ($protected in @('gamePath','vanillaPath','modsPath')) {
            if ($paths[$protected] -and ((Is-Inside $paths[$key] $paths[$protected]) -or (Is-Inside $paths[$protected] $paths[$key]))) {
                Report 'ERROR' "$key overlaps $protected; choose separate development/output locations."
            }
        }
        Report 'INFO' "$key resolves to $($paths[$key]); not created or checked for write access."
    }
    if ((Is-Inside $paths.workPath $paths.outputPath) -or (Is-Inside $paths.outputPath $paths.workPath)) {
        Report 'ERROR' 'workPath and outputPath overlap; choose separate directories.'
    }
    if (-not $paths.modsPath) { Report 'INFO' 'modsPath is blank; installation is not configured or authorized.' }
    elseif (-not (Test-Path -LiteralPath $paths.modsPath -PathType Container)) { Report 'WARN' 'modsPath does not exist; this does not block local creation.' }
    $xmltestReady = $false
    if ($null -eq $config.tools -or $config.tools -isnot [PSCustomObject]) {
        Report 'ERROR' 'tools must be an object with xmltest, lua and python strings.'
    } else {
        foreach ($key in @('xmltest','lua','python')) {
            if (-not (Has-String $config.tools $key)) { Report 'ERROR' "tools.$key must be a JSON string."; continue }
            $tool = Resolve-LocalPath $config.tools.$key $base
            if (-not $tool) { Report 'WARN' "$key is not configured; related checks are unavailable. No tool was installed." }
            elseif ($key -eq 'xmltest' -and [IO.Path]::GetFileName($tool) -ine 'xmltest.exe') { Report 'ERROR' 'Select the Anno 1800 xmltest.exe, not xmltest2.exe or another executable.' }
            elseif (-not (Test-Path -LiteralPath $tool -PathType Leaf)) { Report 'WARN' "$key executable is missing; related checks are unavailable." }
            else {
                Report 'OK' "$key executable is present; inspect version/provenance before execution."
                if ($key -eq 'xmltest') { $xmltestReady = $true }
            }
        }
    }
    if ($script:Issues -gt 0) { Report 'INFO' 'Resolve setup errors before game-dependent work.'; exit 1 }
    Report 'OK' 'Required file-presence checks passed. Audit content/freshness before choosing a patch.'
    if (-not $xmltestReady) { Report 'WARN' 'Offline loader validation is unavailable; do not report it as passed.' }
    Report 'INFO' 'No files written, tools launched, or game/multiplayer tests run.'
    exit 0
} catch { Report 'ERROR' ('Could not inspect configuration or paths: ' + $_.Exception.Message); exit 1 }
