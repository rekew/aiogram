from openai import OpenAI
from aiogram import Dispatcher, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as aioredis
import asyncio

bot = Bot(token = '8186742708:AAGn6fXRKFOw5-ms-AJqGFVxmlTkkIOfZbE')
ai = OpenAI(api_key='f7c0ce4c5786474c9e8a63bca23fd683', base_url='https://api.aimlapi.com/v1')
storage = RedisStorage.from_url('redis://localhost:6379')
dp = Dispatcher(storage=storage)

redis = None

async def setup_redis():
    global redis
    redis = await aioredis.from_url('redis://localhost:6379')

class getAssist(StatesGroup):
    user = State()

@dp.message(Command('start'))
async def start_bot(msg : Message):
    await msg.answer('Hello!')

@dp.message(Command('assist'))
async def give_help(msg : Message, state : FSMContext):
    await state.set_state(getAssist.user)
    await msg.answer('Please send me prompt!')

async def check_call(id: int, limit: int = 3, blockTime: int = 10):
    if await redis.exists('Timer'):
        return False
    key = f'rate_limit:{id}'
    count = await redis.incr(key)
    print(count)
    if count > limit:
        await redis.setex('Timer', 60, 'time is running')
        await redis.delete(key)
        return False
    return True


@dp.message(getAssist.user)
async def answer_prompt(msg : Message, state : FSMContext):
    if not await check_call(msg.from_user.id):
        await msg.answer('⛔ Вы превысили лимит запросов! Подождите 60 секунд и попробуйте снова.')
        return
    await state.clear()
    response = ai.chat.completions.create(
        model = 'mistralai/Mistral-7B-Instruct-v0.2',
        messages = [
            {'role' : 'system', 'content' : 'You are a helpful assistant'},
            {'role' : 'user', 'content' : msg.text},
        ],
    )
    await msg.answer(response.choices[0].message.content)

async def main():
    await setup_redis()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())