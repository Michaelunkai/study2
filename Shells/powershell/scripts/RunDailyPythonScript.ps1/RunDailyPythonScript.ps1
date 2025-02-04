# Define the path to your Python script
$pythonScriptPath = "C:\study\Credentials\youtube\youtubeUploader\5rm.py"

# Get the current date and time
$currentDateTime = Get-Date

# Calculate the time for next execution (4 p.m.)
$nextExecutionTime = Get-Date -Year $currentDateTime.Year -Month $currentDateTime.Month -Day $currentDateTime.Day -Hour 16 -Minute 0 -Second 0

# Calculate the time difference until next execution
$timeDifference = $nextExecutionTime - $currentDateTime

# Create a new scheduled task using Task Scheduler
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "$pythonScriptPath"
$trigger = New-ScheduledTaskTrigger -Once -At $nextExecutionTime
Register-ScheduledTask -TaskName "RunDailyPythonScript" -Action $action -Trigger $trigger
