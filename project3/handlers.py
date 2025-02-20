from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import Command
from database import getTask

router = Router()

@router.message(Command('start'))
async def start_bot(message : Message):
    await message.answer('''Hello! I'm simple to-do list bot.
Please type /help for more instructions
''', reply_markup=ReplyKeyboardRemove())

@router.message(Command('help'))
async def send_help(message : Message):
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text = 'add task')],
        [KeyboardButton(text = 'list of tasks')],
        [KeyboardButton(text = 'delete task')],
    ],
    resize_keyboard= True
    )
    await message.answer('Here is list of all commands:', reply_markup=keyboard)

@router.message(F.text == 'list of tasks')
async def getListOfTasks(msg : Message):
    rows = await getTask(msg.from_user.id)

    if not rows:
        await msg.answer('You have no tasks yet!')
        return
    response = "📋 **Here are your tasks:**\n\n"
    for index, r in enumerate(rows, start=1):
        response += f"🔹 **Task {index}:**\n"
        response += f" 📌 **Name:** {r['name']}\n"
        response += f" 📝 **Description:** {r['description']}\n"
        response += f" 📅 **Deadline:** {r['deadline'].strftime('%Y-%m-%d')}\n"
        response += f" 🔔 **Notify:** {'✅ Yes' if r['notify'] else '❌ No'}\n\n"

    await msg.answer(response, parse_mode="Markdown")
