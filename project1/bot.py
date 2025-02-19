from aiogram import F, Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message
from config import token
import asyncio

bot = Bot(token = token)
dp = Dispatcher()

@dp.message(Command('start'))
async def start_bot(msg : Message):
    await msg.answer('''Привет, я бот который отправляет то же сообщение, который ты напишешь!
Попробуй мне отправить любое сообщение кроме команды '/start', но не отправляй пустые сообщение.
''')

@dp.message(F.text)
async def echo(msg : Message):
    await msg.answer(msg.text)

async def main():
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())