from aiogram import Bot, Dispatcher
from handlers import router as routerHandler
from states import router as routerStates
from notifier import start_scheduler
import asyncio
from database import startDatabase, closeDatabase

dp = Dispatcher()
bot = Bot(token = '8034597869:AAHdnTrNqx57FnJhmu8rgs_kEbJYIdTdG7s')

async def main():
    await startDatabase()
    await start_scheduler() 

    try:
        dp.include_router(routerHandler)
        dp.include_router(routerStates)
        
        await dp.start_polling(bot)
    finally:
        await closeDatabase()

if __name__ == '__main__':
    asyncio.run(main())