-- Keep registration stable when the function library is reloaded.
MyFeature = MyFeature or {}

function MyFeature.onSessionEnter()
    -- Re-evaluate current session state here; no gameplay action in this example.
end

if not MyFeature.sessionEnterCallback then
    MyFeature.sessionEnterCallback = function(...)
        local ok, err = pcall(MyFeature.onSessionEnter, ...)
        if not ok then
            local file = io.open("logs/my_feature_errors.txt", "a")
            if file then
                file:write(tostring(err), "\n")
                file:close()
            end
        end
    end
    table.insert(event.OnSessionEnter, MyFeature.sessionEnterCallback)
end
