from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from database import insertUser, getRole, CreateTable, closeConnection
import asyncio

bot = Bot(token = '8186742708:AAGn6fXRKFOw5-ms-AJqGFVxmlTkkIOfZbE')
dp = Dispatcher()
price = [LabeledPrice(label='Подписка на 1 месяц', amount=50000)]


@dp.message(Command('start'))
async def start_bot(msg : Message):
    await insertUser(msg.from_user.id)
    await msg.answer("Hello! I'm simple bot which divides people by roles!\nType /help to check all commands")

@dp.message(Command('help'))
async def send_help(msg : Message):
    await msg.answer('''
/start - to start bot
/help - to get help
/role - to check out your role
/roles - list of roles
''')

@dp.message(Command('role'))
async def send_role(msg : Message):
    row = await getRole(msg.from_user.id)
    await msg.answer(f"Your current role is: {row["role"]}")

@dp.message(Command('roles'))
async def send_list(msg : Message):
    await msg.answer('''
Here are the list of roles:
member - default role
premium - premium role
moderator - company moderator
admin - company admin
owner - company owner
''')

@dp.message(Command('buy'))
async def buy(msg : Message):
    await bot.send_invoice(
        msg.chat.id,
        title = 'Подписка',
        description = 'Оплата роли',
        provider_token='test_b18SBAaaDCsi9rHDHFjcfbhXVbX8SsMrBU2dn7703kU',
        currency='RUB',
        prices=price,
        start_parameter='subscription',
        payload='subscription_payload'
    )

@dp.pre_checkout_query()
async def checkout(check:PreCheckoutQuery):
    await bot.answer_pre_checkout_query(check.id, ok = True)

@dp.message(F.successful_payment)
async def payment_ok(msg : Message):
    await msg.answer('Спасибо за оплату! Доступ активирован ✅')

async def main():
    await CreateTable()
    try:
        await dp.start_polling(bot)
    finally:
        await closeConnection()


if __name__ == '__main__':
    asyncio.run(main())