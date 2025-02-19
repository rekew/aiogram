from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

keyboard = ReplyKeyboardMarkup(keyboard= [
    [KeyboardButton(text = 'Каталог')],
    [KeyboardButton(text = 'Корзина'), KeyboardButton(text = 'Контакты')],
], 
    resize_keyboard=True,
    input_field_placeholder='Выбери пункт!'
)

callback_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'bmw', callback_data='bmw'), InlineKeyboardButton(text='Toyota', callback_data='toyota')]
])

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Yotube', url = 'https://youtube.com')],
])

anime = ['One Piece', 'JJK', 'Darling in the Franxx', 'One punch man']

async def inline_builder():
    builder = InlineKeyboardBuilder()
    for name in anime:
        builder.add(InlineKeyboardButton(text = name, url = 'https://jut.su'))
    return builder.adjust(2).as_markup()

#The difference between builder and default markup is that markup doesn't have add method while builder does
#adjust makes limit of how much buttons are can be in one row