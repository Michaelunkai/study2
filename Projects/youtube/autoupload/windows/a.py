import os
import sys
from apscheduler.schedulers.blocking import BlockingScheduler

def run_script():
    os.chdir("C:\\study\\Credentials\\youtube\\youtubeUploader")
    os.system("python 5rm.py")

scheduler = BlockingScheduler()
scheduler.add_job(run_script, 'cron', hour=16, minute=1) 
scheduler.start()
