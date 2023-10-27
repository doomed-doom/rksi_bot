from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from functionals.logging import logging, student

#
log_router = Router()


class Login(StatesGroup):
    login = State()
    password = State()


@log_router.message(Command("login"))
async def register_start(message: types.Message, state):
    if not student.check_user_session(message.from_user.id):
        await state.set_state(Login.login)
        await message.answer("Введите логин.")
    else:
        await message.answer("Вы уже вошли в систему.\nПодсказка: /leave - для выхода из системы")


@log_router.message(Login.login)
async def enter_password(message: types.Message, state):
    login = message.text
    await state.update_data(login=login)
    await state.set_state(Login.password)
    await message.answer("Введите пароль.")


@log_router.message(Login.password)
async def enter_password(message: types.Message, state: FSMContext):
    password = message.text

    await state.update_data(password=password)
    data = await state.get_data()

    result = await logging.check_user(data['login'], data['password'])
    if not result:
        await state.clear()
        return await message.answer(text='Неправильный логин или пароль.')
    await logging.update_user_session(message.from_user.id, result[0][0])
    await message.answer(text='Вы успешно вошли в систему.')
    await state.clear()
