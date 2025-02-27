import asyncio
import stripe
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

bot = Bot(token='8186742708:AAGn6fXRKFOw5-ms-AJqGFVxmlTkkIOfZbE')
dp = Dispatcher()

stripe.api_key = 'sk_test_51QvicjP3vgqUAZyXtgnzfaYihnyQQNLsDBdPiUKK9PLkFr5jbYlzqTE2xY8wV3VU21u3tavNvSEItbQwyarNvQA400lu7IUDLp'

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Отправь /buy для покупки подписки.")

@dp.message(Command("buy"))
async def buy(message: Message):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'Подписка на бота'},
                'unit_amount': 0,  
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://yourbot.com/success',
        cancel_url='https://yourbot.com/cancel',
    )
    await message.answer(f"Оплатите по ссылке: {session.url}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
