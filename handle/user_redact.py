from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from functionals.another import groups, keyboard_chunks
from functionals.inlines import user_role_inline
from functionals.logging import start_user, schedule

#
users_router = Router()


class Users(StatesGroup):
    user_req = State()
    change_login = State()
    change_password = State()
    change_session = State()
    change_group = State()


@users_router.message(Users.user_req)
async def find_users(message: types.Message, state: FSMContext):
    username = message.text

    user = await start_user.find_user(username)

    for i in user:
        role = i[1]
        username = i[2]
        await state.update_data(username=username)
        if role != 'owner':
            await message.answer(f"Выберите действие для @{username}", reply_markup=user_role_inline())
        else:
            await message.answer("Вы не можете менять роль у создателя!")


@users_router.message(Users.change_login)
async def find_users(message: types.Message, state: FSMContext):
    new_login = message.text

    data = await state.get_data()

    old_login = data['login']

    await start_user.change_attribute('login', old_login, new_login)

    await message.answer(f"Вы успешно поменяли логин с {old_login} на {new_login}!")
    await state.clear()


@users_router.message(Users.change_password)
async def find_users(message: types.Message, state: FSMContext):
    new_password = message.text

    data = await state.get_data()

    old_login = data['login']

    await start_user.change_attribute('password', old_login, new_password)

    await message.answer(f"Вы успешно поменяли пароль на {new_password}!")
    await state.clear()


@users_router.message(Users.change_group)
async def find_users(message: types.Message, state: FSMContext):
    if message.text in groups(schedule.get_group_count()):
        new_group = message.text

        data = await state.get_data()

        old_login = data['login']

        await start_user.change_attribute('main_group', old_login, new_group)

        await message.answer(f"Вы успешно поменяли группу на {new_group}!", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer("Вы указали несуществующую группу.",
                             reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_chunks(schedule.get_group_count())))
