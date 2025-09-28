from apscheduler.schedulers.asyncio import AsyncIOScheduler
from userbot_worker import send_ads

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.start()

def schedule_ads(account, groups, message, interval):
    scheduler.add_job(send_ads, 'interval', minutes=interval, args=[account, groups, message])
