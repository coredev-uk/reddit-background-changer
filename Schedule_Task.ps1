# Schedule_Task.ps1

# Register the new PowerShell scheduled task

# The name of your scheduled task.
$taskName = "ExportAppLog"
$taskPath = "Custom Tasks/Reddit Background Changer"

# Describe the scheduled task.
$description = "Export the 10 newest events in the application log"

# Register the scheduled task
Register-ScheduledTask `
    -TaskName $taskName `
    -TaskPath $taskPath `
    -Action $taskAction `
    -Trigger $taskTrigger `
    -Description $description

    https://docs.microsoft.com/en-us/powershell/module/scheduledtasks/register-scheduledtask?view=winserver2012r2-ps
    https://devblogs.microsoft.com/scripting/use-powershell-to-create-scheduled-tasks/
    https://xplantefeve.io/posts/SchdTskOnEvent