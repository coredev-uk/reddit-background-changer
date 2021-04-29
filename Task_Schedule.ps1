# Schedule_Task.ps1

Write-Host 'Please ensure that this script is located in the same directory as main.py.'
Write-Host 'Would you like to conintue creating the scheduled task?'
$Confirmation = Read-Host
$Confirmation = $Confirmation.ToLower()

if ($Confirmation -ne 'yes') {
    exit
}

$xmlPath = $PSScriptRoot + '\bin\rbc.xml'
Write-Host $xmlPath

Write-Host 'Generating Task...'
Register-ScheduledTask -xml (Get-Content ($PSScriptRoot + '\bin\rbc.xml') | Out-String) -TaskName 'Reddit Background Changer' -TaskPath '\Custom Tasks\'

$ActionParameters = @{
    Execute  = ("$PSScriptRoot + 'venv\scripts\pythonw.exe'")
    Argument = 'main.py'
    WorkingDirectory = $PSScriptRoot
}

$Frequency = Read-Host 'How often would you like your background to change?'
Write-Host 'Available Values:'
Write-Host '- Daily'
Write-Host '- Weekly'
Write-Host '(case sensitive)'

if ($Frequency -ne 'Daily' -Or $Frequency -ne 'Weekly') {
    exit
}
$Action = New-ScheduledTaskAction @ActionParameters
$Trigger = New-ScheduledTaskTrigger -$Frequency -AtLogOn
$RegSchTaskParameters = @{
    TaskName    = 'Reddit Background Changer'
    Action      = $Action
    Trigger     = $Trigger
}

Set-ScheduledTask $RegSchTaskParameters

# https://docs.microsoft.com/en-us/powershell/module/scheduledtasks/register-scheduledtask?view=winserver2012r2-ps
# https://devblogs.microsoft.com/scripting/use-powershell-to-create-scheduled-tasks/
# https://xplantefeve.io/posts/SchdTskOnEvent