-- Generic helper: submit/read/isDone are supplied by an audited feature.
local function waitForObservedChange(submit, read, isDone, maxYields)
    submit()
    for attempt = 1, maxYields do
        coroutine.yield()
        local value = read()
        if isDone(value) then
            return true, value
        end
    end
    return false, "change was not observed within the configured bound"
end
