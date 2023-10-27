from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from functionals.logging import spam_user

#
spam_router = Router()


class Spam(StatesGroup):
    text = State()
    text_group = State()
    text_user = State()


@spam_router.message(Spam.text)
async def spam_all(message: types.Message, state: FSMContext, bot):
    text = message.text

    users = await spam_user.spam_all()
    for user in users:
        await bot.send_message(user[0], text)

    await state.clear()


@spam_router.message(Spam.text_group)
async def spam_user_group(message: types.Message, state: FSMContext, bot):
    text = message.text
    data = await state.get_data()

    users = await spam_user.spam_group(data['group_name'])

    for user in users:
        if user[0]:
            await bot.send_message(user[0], text)

    await state.clear()


@spam_router.message(Spam.text_user)
async def spam_reg_user(message: types.Message, state: FSMContext, bot):
    text = message.text

    users = await spam_user.spam_user_all()
    for user in users:
        if user[0]:
            await bot.send_message(user[0], text)

    await state.clear()
