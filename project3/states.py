from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import Router, F
from database import insertTask, getTask, remove_task_from_db
from datetime import datetime

class AddTaskState(StatesGroup):
    name = State()
    description = State()
    deadline = State()
    notify = State()

class RemoveTaskState(StatesGroup):
    number = State()

router = Router()

@router.message(F.text == 'add task')
async def add_task(msg: Message, state: FSMContext):
    await state.set_state(AddTaskState.name)
    await msg.answer('How are you gonna call the name of task?', reply_markup=ReplyKeyboardRemove())

@router.message(AddTaskState.name)
async def add_task_state_one(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await state.set_state(AddTaskState.description)
    await msg.answer('Now please provide the description for task')

@router.message(AddTaskState.description)
async def add_task_state_two(msg: Message, state: FSMContext):
    await state.update_data(description=msg.text)
    await state.set_state(AddTaskState.deadline)
    await msg.answer('''What is the deadline?
Please write the date in YEAR-MONTH-DAY format. Example:
2025-06-15
If you enter it incorrectly, the notification might not work.
''')

@router.message(AddTaskState.deadline)
async def add_task_state_three(msg: Message, state: FSMContext):
    try:
        await state.update_data(deadline=datetime.strptime(msg.text, "%Y-%m-%d").date())
        await state.set_state(AddTaskState.notify)
        keyboard = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='Yes')],
            [KeyboardButton(text='No')],
        ], resize_keyboard=True, input_field_placeholder='Yes or No?')
        await msg.answer('Do you want me to remind you after the deadline is passed?', reply_markup=keyboard)
    except ValueError:
        await msg.answer("Invalid date format. Please try again (YEAR-MONTH-DAY).")

@router.message(AddTaskState.notify)
async def add_task_state_final(msg: Message, state: FSMContext):
    ans = msg.text.lower() == 'yes'
    await state.update_data(notify=ans)
    data = await state.get_data()
    await insertTask(data, msg.from_user.id)
    await msg.answer(f'''The task is added successfully!
Here is the info:
📌 Name: {data["name"]}
📝 Description: {data["description"]}
📅 Deadline: {data["deadline"]}
🔔 Notify: {'✅ Yes' if data["notify"] else '❌ No'}
''', reply_markup=ReplyKeyboardRemove())
    await state.clear()

@router.message(F.text == 'delete task')
async def delete_task_one(msg: Message, state: FSMContext):
    await state.set_state(RemoveTaskState.number)
    
    rows = await getTask(msg.from_user.id)

    if not rows:
        await msg.answer("You have no tasks yet!")
        return

    response = "📋 **Here are your tasks:**\n\n"
    for index, r in enumerate(rows, start=1):
        response += f"🔹 **Task {index}:**\n"
        response += f" 📌 **Name:** {r['name']}\n"
        response += f" 📝 **Description:** {r['description']}\n"
        response += f" 📅 **Deadline:** {r['deadline'].strftime('%Y-%m-%d')}\n"
        response += f" 🔔 **Notify:** {'✅ Yes' if r['notify'] else '❌ No'}\n\n"


    await state.update_data(task_list=rows)
    await msg.answer(f"Which task would you like to delete?\nType the task number (e.g., '1' to delete the first task).\n{response}", 
                     reply_markup=ReplyKeyboardRemove())

@router.message(RemoveTaskState.number)
async def delete_task_two(msg: Message, state: FSMContext):
    try:
        index = int(msg.text) - 1
        data = await state.get_data()
        tasks = data.get("task_list", [])

        if index < 0 or index >= len(tasks):
            await msg.answer("Invalid task number! Please try again.")
            return
        
        task_id = tasks[index]['index']
        
        deleted = await remove_task_from_db(task_id)

        if deleted:
            await msg.answer(f"✅ Task **'{tasks[index]['name']}'** was deleted successfully!")
        else:
            await msg.answer("⚠️ Something went wrong. Task might not exist.")
    except ValueError:
        await msg.answer("❌ Invalid input. Please enter a number.")
    
    await state.clear()
