from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import asyncio

bot = Bot(token='8097487442:AAHKVvqATwOCPxBZ8Fb9Gm0gw9iKsMK5eto')
dp = Dispatcher()

class Form(StatesGroup):
    name = State()
    birth_date = State()
    gender = State()
    city = State()
    height_weight = State()
    acting_experience = State()
    acting_experience_detail = State()
    appearance = State()
    skills = State()
    photos = State()
    video = State()
    contacts = State()

gender_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Мужчина"), KeyboardButton(text="Женщина"), KeyboardButton(text="Другой")]
    ],
    resize_keyboard=True
)

experience_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
    ],
    resize_keyboard=True
)

skip_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Пропустить")]
    ],
    resize_keyboard=True
)


@dp.message(Command('start'))
async def start_bot(message: Message):
    start_keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Оставить заявку')]
    ], resize_keyboard=True)
    await message.answer('Привет!', reply_markup=start_keyboard)

@dp.message(F.text == 'Оставить заявку')
async def state_start(msg: Message, state: FSMContext):
    await msg.answer('Введи своё *Имя и Фамилию*.', parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.name)

@dp.message(Form.name)
async def process_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer('📅 Укажи дату рождения (в формате ДД.ММ.ГГГГ)')
    await state.set_state(Form.birth_date)

@dp.message(Form.birth_date)
async def process_birth_date(msg: Message, state: FSMContext):
    await state.update_data(birth_date=msg.text)
    await msg.answer("🚻 Выбери пол:", reply_markup=gender_kb)
    await state.set_state(Form.gender)

@dp.message(Form.gender)
async def process_gender(msg: Message, state: FSMContext):
    await state.update_data(gender=msg.text)
    await msg.answer('🏙 В каком городе ты живёшь?', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.city)

@dp.message(Form.city)
async def process_city(msg: Message, state: FSMContext):
    await state.update_data(city=msg.text)
    await msg.answer('📏 Введи свой рост и вес (например: 175 см, 70 кг)')
    await state.set_state(Form.height_weight)

@dp.message(Form.height_weight)
async def process_height_weight(msg: Message, state: FSMContext):
    await state.update_data(height_weight=msg.text)
    await msg.answer('🎭 Есть ли у тебя актёрский опыт?', reply_markup=experience_kb)
    await state.set_state(Form.acting_experience)

@dp.message(Form.acting_experience)
async def process_experience(msg: Message, state: FSMContext):
    if msg.text == 'Да':
        await msg.answer('Опиши свой актерский опыт (примеры работ)', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.acting_experience_detail)
    else:
        await state.update_data(acting_experience="Нет")  
        await msg.answer('Окей, двигаемся дальше', reply_markup=ReplyKeyboardRemove())
        await msg.answer('🧏‍♂️ Есть ли у тебя особые внешние особенности? (Шрамы, борода и т. д.)')
        await state.set_state(Form.appearance)

@dp.message(Form.acting_experience_detail)
async def process_experience_text(msg: Message, state: FSMContext):
    await state.update_data(acting_experience=msg.text)  
    await msg.answer('🧏‍♂️ Есть ли у тебя особые внешние особенности? (Шрамы, борода и т. д.)')
    await state.set_state(Form.appearance)

@dp.message(Form.appearance)
async def process_appearance(msg: Message, state: FSMContext):
    await state.update_data(appearance=msg.text)
    await msg.answer('🎤 Укажи свои навыки (акробатика, вокал, фехтование и т. д.)')
    await state.set_state(Form.skills)

@dp.message(Form.skills)
async def process_skills(msg: Message, state: FSMContext):
    await state.update_data(skills=msg.text)
    await msg.answer('📸 Отправь несколько фото (до 3-х штук)')
    await state.set_state(Form.photos)

@dp.message(F.photo, Form.photos)
async def process_photos(msg: Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get('photos', [])
    photos.append(msg.photo[-1].file_id)

    if len(photos) >= 3:
        await state.update_data(photos=photos)
        await msg.answer("📽 Хочешь загрузить видеовизитку?", reply_markup=skip_kb)
        await state.set_state(Form.video)
    else:
        await state.update_data(photos=photos)
        await msg.answer('Отправь ещё фото или напиши /next, если достаточно.')

@dp.message(Command('next'))
async def skip_photos(msg: Message, state: FSMContext):
    await msg.answer('📽 Хочешь загрузить видеовизитку?', reply_markup=skip_kb)
    await state.set_state(Form.video)

@dp.message(F.video, Form.video)
async def process_video(msg: Message, state: FSMContext):
    await state.update_data(video=msg.video.file_id)
    await msg.answer('📱 Введи свои контактные данные (номер телефона, соцсети)', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.contacts)

@dp.message(Form.video)
async def skip_video(msg: Message, state: FSMContext):
    await msg.answer('📱 Введи свои контактные данные (номер телефона, соцсети)', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.contacts)

@dp.message(Form.contacts)
async def process_contacts(msg: Message, state: FSMContext):
    await state.update_data(contacts=msg.text)
    data = await state.get_data()
    profile_text = f"""
📛 *Имя:* {data.get('name', 'Не указано')}
📅 *Дата рождения:* {data.get('birth_date', 'Не указано')}
🚻 *Пол:* {data.get('gender', 'Не указано')}
🏙 *Город:* {data.get('city', 'Не указано')}
📏 *Рост/Вес:* {data.get('height_weight', 'Не указано')}
🎭 *Актёрский опыт:* {data.get('acting_experience', 'Нет')}
🧏‍♂️ *Особенности:* {data.get('appearance', 'Не указано')}
🎤 *Навыки:* {data.get('skills', 'Не указано')}
📱 *Контакты:* {data.get('contacts', 'Не указано')}
"""

    await msg.answer(profile_text, parse_mode='Markdown')
    await state.clear()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
