from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from functionals.another import groups, keyboard_chunks
from functionals.logging import unloging, schedule, student

#
reg_router = Router()


class Register(StatesGroup):
    login = State()
    password = State()
    main_group = State()


@reg_router.message(Command("register"))
async def register_start(message: types.Message, state):
    if not student.check_user_session(message.from_user.id):
        await state.set_state(Register.login)
        await message.answer("Введите логин.")
    else:
        await message.answer("Вы уже вошли в систему.\nПодсказка: /leave - для выхода из системы")


@reg_router.message(Register.login)
async def enter_password(message: types.Message, state):
    login = message.text
    await state.update_data(login=login)
    await state.set_state(Register.main_group)
    await message.answer("Выберите вашу группу.",
                         reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_chunks(schedule.get_group_count())))


@reg_router.message(Register.main_group)
async def enter_group(message: types.Message, state: FSMContext):
    if message.text in groups(schedule.get_group_count()):
        main_group = message.text
        await state.update_data(main_group=main_group)
        await state.set_state(Register.password)
        await message.answer("Введите пароль.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Вы указали несуществующую группу.",
                             reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_chunks(schedule.get_group_count())))


@reg_router.message(Register.password)
async def enter_password(message: types.Message, state: FSMContext):
    password = message.text
    await state.update_data(password=password)
    data = await state.get_data()
    if len(data['password']) >= 8:
        await unloging.register(message, data)
        await state.clear()
    else:
        await message.answer("Пароль не соответствует требованиям.\nМинимальная длина пароля 8 символов.")

