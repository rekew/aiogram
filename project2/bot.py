from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
from database import initDb, botToken, insertUser, getUsers

bot = Bot(token = botToken)
dp = Dispatcher()

@dp.message(Command('start'))
async def start_bot(msg : Message):
    await insertUser(msg.from_user.id)
    await msg.answer('''
    Hello! I'm a simple bot with command /users and /start
Try to use command '/users' and you will see all id of People that had chat with me!
    ''')

@dp.message(Command('users'))
async def get_users(msg : Message):
    rows = await getUsers()

    if rows:
        users = []
        for user in rows:
            users.append(str(user['id']))
        response = "Users who have chatted with me:\n" + "\n".join(users)
    else:
        response = 'No users found.'

    await msg.answer(response)

@dp.message(F.text)
async def send_message(msg : Message):
    await msg.reply('''
Try to use commands:
/users - to get all users id
/start - to get intro message
''')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())