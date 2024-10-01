import os
import subprocess

# Path to the Python script you want to run
script_path = r"C:\study\credentials\youtube\youtubeuploader\5rm.py"

# Command to create a scheduled task
task_cmd = f'schtasks /create /sc daily /tn "RunYouTubeUploader" /tr "python {script_path}" /st 14:05 /ru micha'

# Run the command to create the scheduled task
subprocess.run(task_cmd, shell=True)
