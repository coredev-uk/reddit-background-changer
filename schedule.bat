@REM CHANGE
@REM THIS
@REM TO POWERSHELL

@echo off

py -3 --version
if ERRORLEVEL 1 (echo "No Python3 Install has been found. Please install Python3 and try again." EXIT /B)

SET current_dir = %~dp0
if not exist %current_dir% + main.py (echo "main.py not found! Please make sure they are in the same directory." EXIT /B)
SET pyFile = %current_dir% + main.py


echo "This script will automatically create a shortcut in Task Scheduler for this script. Please make sure you are running this file in the same directory as main.py and with the files in the location it will remain and having configured your config.py file."
SET /P _inputname= Would you like to continue?:
IF "%_inputname%"=="YES" GOTO : create_scheduled_event
ECHO Closing.
GOTO :end
:create_scheduled_event
ECHO Creating Event...
SET /P _sc= How often would you like this script to run? (HOURLY, DAILY, WEEKLY, MONTHLY):

IF "%_sc%"=="WEEKLY" GOTO : WEEKLY_EVENT
IF "%_sc%"=="MONTHLY" GOTO : MONTHLY_EVENT
IF "%_sc%"=="HOURLY" GOTO : HOURLY_EVENT

:WEEKLY_EVENT
SET /P _day= What day of the week would you like this script to run? (MON, TUE, WED, THU, FRI, SAT, or SUN)
SCHTASKS /CREATE /SC %_sc% /SC ONLOGON /DELAY 0000:30 /D %_day% /TN "Custom Tasks\Reddit Background Changer" /TR pyFile /ST 00:00
pythonw main.py

:MONTHLY_EVENT
SET /P _day= What day of the month would you like this to run on? (1-31 or * if you would like it to be everyday)
SCHTASKS /CREATE /SC %_sc% /SC ONLOGON /DELAY 0000:30 /D %_day% /TN "Custom Tasks\Reddit Background Changer" /TR pyFile /ST 00:00
pythonw main.py

:HOURLY_EVENT
SCHTASKS /CREATE /SC %_sc% /SC ONLOGON /DELAY 0000:30 /D %_day% /TN "Custom Tasks\Reddit Background Changer" /TR pyFile /ST 00:00
pythonw main.py

:end