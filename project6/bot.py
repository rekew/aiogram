from aiogram import Dispatcher, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio
import redis

bot = Bot(token = '8186742708:AAGn6fXRKFOw5-ms-AJqGFVxmlTkkIOfZbE')
dp = Dispatcher()

class Reg(StatesGroup):
    name = State()
    date = State()
    confirm = State()

@dp.message(Command('start'))
async def start_bot(msg : Message):
    await msg.answer('Привет! Я бот для бронирования. Вы можете записаться на сеанс или управлять своими бронированиями. Используйте команду /help для подробностей.')

@dp.message(Command('help'))
async def send_help(msg : Message):
    kb = InlineKeyboardMarkup(inline_keyboard=([
        [InlineKeyboardButton(text='📅 Запись на сеанс', callback_data='record')],
        [InlineKeyboardButton(text='🛠 Управление бронированиями', callback_data='settings')],
        [InlineKeyboardButton(text='💳 Оплата услуг', callback_data='payment')]
    ]))
    await msg.answer('Вот что я умею:', reply_markup=kb)
    await msg.answer('Выберите нужную опцию')

@dp.callback_query(F.data == 'record')
async def registration(call : CallbackQuery, state : FSMContext):
    await state.set_state(Reg.name)
    await call.message.answer('Введите ваше имя для регистрации:')

@dp.message(Reg.name)
async def process_name(msg : Message, state : FSMContext):
    await state.update_data(name = msg.text)
    await state.set_state(Reg.date)
    await msg.answer('Выберите дату и время для записи.')

@dp.message(Reg.date)
async def process_date(msg : Message, state : FSMContext):
    await state.update_data(date = msg.text)
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text = 'Да'), KeyboardButton(text = 'Нет')]
    ], resize_keyboard=True
    )
    await msg.answer('Подтвердите запись:', reply_markup=kb)
    await state.set_state(Reg.confirm)

@dp.message(Reg.confirm)
async def confirm_reg(msg : Message, state : FSMContext):
    if msg.text.lower() == 'нет':
        await msg.answer('Регистрация отменена!', reply_markup=ReplyKeyboardRemove())
    else:
        data = await state.get_data()
        await msg.answer(f"Спасибо {data.get('name')}! Вы успешно записались на дату: {data.get('date')}", reply_markup=ReplyKeyboardRemove())
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())