from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from functionals.another import keyboard_chunks, groups
from functionals.logging import student, schedule

#
del_router = Router()


class Delete(StatesGroup):
    login = State()
    main_group = State()
    password = State()


@del_router.message(Command("delete"))
async def register_start(message: types.Message, state):
    if student.check_user_session(message.from_user.id):
        await state.set_state(Delete.login)
        await message.answer("Чтобы удалить ваш аккаунт, нужно убедиться что это именно вы.\nВведите ваш логин.")
    else:
        await message.answer("Пожалуйства, сначала войдите в систему.")


@del_router.message(Delete.login)
async def enter_password(message: types.Message, state):
    login = message.text
    await state.update_data(login=login)
    await state.set_state(Delete.main_group)
    await message.answer("Выберите вашу группу.",
                         reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_chunks(schedule.get_group_count())))


@del_router.message(Delete.main_group)
async def enter_group(message: types.Message, state: FSMContext):
    if message.text in groups(schedule.get_group_count()):
        main_group = message.text
        await state.update_data(main_group=main_group)
        await state.set_state(Delete.password)
        await message.answer("Введите ваш пароль.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Вы указали несуществующую группу.",
                             reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_chunks(schedule.get_group_count())))


@del_router.message(Delete.password)
async def enter_password(message: types.Message, state: FSMContext):
    password = message.text

    await state.update_data(password=password)
    data = await state.get_data()

    result = await student.delete_user_account(data['login'], data['password'], data['main_group'],
                                               message.from_user.id)
    if not result:
        await state.clear()
        return await message.answer(text='Вы ввели неправильные данные.')
    await message.answer(text='Вы успешно удалили аккаунт.')
    await state.clear()
