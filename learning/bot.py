import asyncio
from config import token
import logging
from app.handlers import router
from aiogram import Bot, Dispatcher

bot = Bot(token = token)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')