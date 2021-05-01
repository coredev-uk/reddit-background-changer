@ECHO off
echo "Removing Scheduled Task"
SCHTASKS /DELETE /TN "Custom Tasks\rbc"
SCHTASKS /DELETE /TN "Custom Tasks\rbc-dir-clean"