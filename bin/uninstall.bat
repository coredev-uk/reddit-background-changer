@ECHO off
echo "Removing Scheduled Task"
SCHTASKS /DELETE /TN "Custom Tasks\Reddit Background Changer"
SCHTASKS /DELETE /TN "Custom Tasks\Reddit Background Changer (Directory Cleaner)"