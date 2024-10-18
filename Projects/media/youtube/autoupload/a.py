import os
import sys
from apscheduler.schedulers.blocking import BlockingScheduler

def run_script():
    os.chdir("/home/ubuntu/videos")
    os.system("python3 5rm.py")

scheduler = BlockingScheduler()
scheduler.add_job(run_script, 'cron', hour=16, minute=01)
scheduler.start()
