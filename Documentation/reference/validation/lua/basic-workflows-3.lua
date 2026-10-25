ExampleAuthor = ExampleAuthor or {}

function ExampleAuthor.logStartup()
    local file = io.open("logs/example_author.txt", "a")
    if file then
        file:write("startup PID=", tostring(ts.Participants.GetGetCurrentParticipantID()),
                   " session=", tostring(session.getSessionGUID()), "\n")
        file:close()
    end
end

local ok, err = pcall(ExampleAuthor.logStartup)
if not ok then
    print("ExampleAuthor startup failed: " .. tostring(err))
end
