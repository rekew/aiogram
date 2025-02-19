from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb

router = Router()

@router.message(CommandStart())
async def start_bot(msg : Message):
    await msg.answer(f'''
Привет {msg.from_user.first_name}, {msg.from_user.last_name}!
Твой ID : {msg.from_user.id}                     
    ''')

@router.message(Command('menu'))
async def send_menu(msg : Message):
    await msg.answer('Выбери действие: ', reply_markup=kb.keyboard)

@router.message(Command('inline'))
async def send_inline_menu(msg : Message):
    await msg.answer('Вот Inline клавиатура:', reply_markup=kb.settings)

@router.message(Command('anime'))
async def send_anime(msg : Message):
    await msg.answer(text = 'Вот список аниме:', reply_markup=await kb.inline_builder())

@router.message(Command('help'))
async def help_bot(msg : Message):
    await msg.reply('это команда /help')

@router.message(F.text == 'Как дела?')
async def how_are_you(msg : Message):
    await msg.reply('ок!')

@router.message(Command('get_photo'))
async def send_photo(msg : Message):
    await msg.answer_photo(photo = 'AgACAgIAAxkBAAMXZ7NsVhgzeMXkyJAKrs7rSztN7I0AAgPtMRs6aJlJe_2zabTLdaIBAAMCAAN5AAM2BA'
 , caption= 'Это твое фото!'                          )

@router.message(F.photo)
async def get_photo(msg : Message):
    await msg.reply(f'ID photo: {msg.photo[-1].file_id}')
    print(msg)

@router.message(Command('cars'))
async def get_cars(msg : Message):
    await msg.reply('Вот список машин', reply_markup=kb.callback_button)

@router.callback_query(F.data == 'bmw')
async def bmw(call : CallbackQuery):
    await call.answer('Уведомление от BMW', show_alert=True)
    await call.message.answer('Ты нажал на BMW!')

@router.callback_query(F.data == 'toyota')
async def toyota(call : CallbackQuery):
    await call.answer('Уведомление от Toyota', show_alert=True)
    await call.message.edit_text('Ты нажал на Toyota', reply_markup=await kb.inline_builder())