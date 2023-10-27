import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery

from functionals.inlines import welcome_inline, admin_panel_inline
from functionals.logging import student, start_user
from functionals.queries import query_callback
from handle import register, login, delete, spamming, documents, user_redact

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

API_TOKEN = "6739011459:AAHWs2mvtEWzJFkDZEOJreRhcY0aio7tLZM"
# Объект бота
bot = Bot(token=API_TOKEN)

# Владелец бота
owner = [6522474018]

# Диспетчер нужен для хэндлеров и их регистрации функций-обработчиков
dp = Dispatcher()

#исключения для роутеров
dp.include_routers(register.reg_router, login.log_router, delete.del_router, spamming.spam_router,
                   documents.document_router, user_redact.users_router)


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await start_user.check_user(message.from_user.id, message.from_user.username)
    if message.from_user.id in owner:
        await start_user.change_role(message.from_user.username, 'owner')
    if student.check_user_session(message.from_user.id):
        main_group = student.check_user_session(message.from_user.id)[0][-1]
        await message.answer("Привет! Выбери опцию:", reply_markup=welcome_inline(main_group))
    else:
        await message.answer("Пожалуйства, сначала войдите в систему.")


@dp.message(Command('panel'))
async def admin_menu(message: types.Message):
    if await start_user.check_user(message.from_user.id):
        await message.answer('Это админ панель.', reply_markup=admin_panel_inline())


@dp.message(Command("leave"))
async def cmd_leave(message: types.Message):
    if student.check_user_session(message.from_user.id):
        await student.leave_user_session(message.from_user.id)
        await message.answer("Вы успешно вышли из системы.")
    else:
        await message.answer("Пожалуйства, сначала войдите в систему.")


# Обработка запросов пользователя при нажатии inline кнопки
@dp.callback_query()
async def callback_query(call: CallbackQuery, state):
    if student.check_user_session(call.message.chat.id):
        main_group = student.check_user_session(call.message.chat.id)[0][-1]
        await query_callback(bot, call, main_group, state)
    elif await start_user.check_user(call.message.message_id):
        await query_callback(bot, call, None, state)
    else:
        await call.message.edit_text("Пожалуйства, сначала войдите в систему.", reply_markup=None)


if __name__ == "__main__":
    # Запуск бота
    asyncio.run(dp.start_polling(bot))
