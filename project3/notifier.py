import asyncio
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import get_tasks_due_today

bot = Bot(token="8034597869:AAHdnTrNqx57FnJhmu8rgs_kEbJYIdTdG7s")

async def send_notifications():
    tasks = await get_tasks_due_today()
    for task in tasks:
        user_id = task['id']
        name = task['name']
        description = task['description']
        message = f"🔔 Reminder: Your task **'{name}'** is due today!\n📌 {description}"
        await bot.send_message(user_id, message)

async def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_notifications, "cron", hour=9)  
    scheduler.start()
