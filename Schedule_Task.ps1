# Schedule_Task.ps1

$ActionParameters = @{
    Execute  = '.env\pythonw.exe'
    Argument = $PSScriptRoot + '-File main.py'
}

$Action = New-ScheduledTaskAction @ActionParameters

$Settings = New-ScheduledTaskSettingsSet

$RegSchTaskParameters = @{
    TaskName    = 'Reddit Background Changer'
    Description = '(empty)'
    TaskPath    = '\Custom Tasks\'
    Action      = $Action
    Settings    = $Settings
    Trigger     = $Trigger
}

Register-ScheduledTask @RegSchTaskParameters

# https://docs.microsoft.com/en-us/powershell/module/scheduledtasks/register-scheduledtask?view=winserver2012r2-ps
# https://devblogs.microsoft.com/scripting/use-powershell-to-create-scheduled-tasks/
# https://xplantefeve.io/posts/SchdTskOnEvent