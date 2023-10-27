from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

from functionals.another import admin_offices, groups, shedule_tuple_student, shedule_tuple_teacher, get_full_day_name, \
    keyboard_chunks
from functionals.inlines import student_inline, others_inline, admin_office_inline, true_links_inline, welcome_inline, \
    teacher_inline, weekdays_inline_teacher, weekdays_inline_student, weekdays_main_inline_student, admin_panel_inline, \
    spamming_inline, spamming_group_inline, docs_group_inline, admin_docs_inline, admin_docs_group_inline, \
    users_redact_inline, admin_accounts_inline, redact_user_inline
from functionals.logging import schedule, files, start_user
from handle.documents import Documents
from handle.spamming import Spam
from handle.user_redact import Users


async def query_callback(bot, call: CallbackQuery, main_group, state: FSMContext):
    # получает запрос, полученный после нажатии кнопки
    if call.data == 'sheldure_student':
        # изменяет кнопки, чтобы сделать удобнее для пользователей
        await bot.edit_message_reply_markup(reply_markup=student_inline(),
                                            chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data in groups(schedule.get_group_count()):
        await bot.edit_message_text(f'Привет! Выбери опцию:',
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id, reply_markup=weekdays_inline_student(call.data))
    elif call.data == 'sheldure_teacher':
        await bot.edit_message_reply_markup(reply_markup=teacher_inline(),
                                            chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data in groups(schedule.get_teacher_count()):
        await bot.edit_message_text(f'Привет! Выбери опцию:',
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id, reply_markup=weekdays_inline_teacher(call.data))
    elif call.data == 'spamming':
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=spamming_inline())
    elif call.data == 'spamming_all':
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=admin_panel_inline())
        await state.set_state(Spam.text)
        await call.message.answer("Введите текст.")
    elif call.data == 'spamming_group':
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=spamming_group_inline())
    elif call.data == 'spamming_users':
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=admin_panel_inline())
        await state.set_state(Spam.text_user)
        await call.message.answer("Введите текст.")
    elif call.data == 'files':
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=admin_docs_inline()
                                            )
    elif call.data == 'add_docs':
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=admin_panel_inline())
        await state.set_state(Documents.text)
        await call.message.answer("Отправьте файл.")
    elif call.data == 'del_docs':
        await bot.edit_message_reply_markup(reply_markup=admin_docs_group_inline(),
                                            chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'users':
        await bot.edit_message_reply_markup(reply_markup=users_redact_inline(),
                                            chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'redact_account':
        await bot.edit_message_reply_markup(reply_markup=admin_accounts_inline(),
                                            chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'redact_role':
        await bot.edit_message_reply_markup(reply_markup=admin_panel_inline(),
                                            chat_id=call.message.chat.id, message_id=call.message.message_id)
        await state.set_state(Users.user_req)
        await call.message.answer("Напишите имя пользователя без @.")
    elif call.data == 'login_change':
        await bot.edit_message_reply_markup(reply_markup=users_redact_inline(),
                                            chat_id=call.message.chat.id, message_id=call.message.message_id)
        await state.set_state(Users.change_login)
        await call.message.answer("Напишите новый логин.")
    elif call.data == 'password_change':
        await bot.edit_message_reply_markup(reply_markup=users_redact_inline(),
                                            chat_id=call.message.chat.id, message_id=call.message.message_id)
        await state.set_state(Users.change_password)
        await call.message.answer("Напишите новый пароль.")
    elif call.data == 'group_change':
        await bot.edit_message_reply_markup(reply_markup=users_redact_inline(),
                                            chat_id=call.message.chat.id, message_id=call.message.message_id)
        await state.set_state(Users.change_group)
        await call.message.answer("Выберите новую группу.", reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard_chunks(schedule.get_group_count())))
    elif call.data == 'session_change':
        await bot.edit_message_reply_markup(reply_markup=users_redact_inline(),
                                            chat_id=call.message.chat.id, message_id=call.message.message_id)
        data = await state.get_data()
        login = data['login']
        await start_user.change_attribute('session_id', login, 0)

        await call.message.answer(f"Вы успешно вышли из устройства с аккаунта {login}!")
        await state.clear()
    elif call.data == 'account_delete':
        await bot.edit_message_reply_markup(reply_markup=users_redact_inline(),
                                            chat_id=call.message.chat.id, message_id=call.message.message_id)
        data = await state.get_data()
        login = data['login']
        await start_user.del_account(login)

        await call.message.answer(f"Вы успешно удалили аккаунт {login}!")
        await state.clear()

    elif call.data == 'role_admin':
        try:
            data = await state.get_data()
            await start_user.change_role(data['username'], "admin")
            await call.message.edit_text(text=f"Изменили роль @{data['username']} на админа.")
            await state.clear()
        except:
            await call.message.edit_text(text="Действие отменено.")
    elif call.data == 'role_member':
        try:
            data = await state.get_data()
            await start_user.change_role(data['username'], "member")
            await call.message.edit_text(text=f"Изменили роль @{data['username']} на участника.")
            await state.clear()
        except:
            await call.message.edit_text(text="Действие отменено.")
    elif call.data == 'cancel_role':
        await call.message.edit_text(text="Вы отменили действие.")
    elif call.data == 'others':
        await bot.edit_message_reply_markup(reply_markup=others_inline(),
                                            chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'admin_offices':
        await bot.edit_message_text(f'Привет! Выбери опцию:', reply_markup=admin_office_inline(),
                                    chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'true_links':
        await bot.edit_message_reply_markup(reply_markup=true_links_inline(),
                                            chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'docs':
        await bot.edit_message_reply_markup(reply_markup=docs_group_inline(),
                                            chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'admin_back':
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id, reply_markup=admin_panel_inline())
    elif call.data == 'Back':
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id, reply_markup=welcome_inline(main_group))
    elif call.data.split("_")[-1] == "main":
        await bot.edit_message_text(f'Привет! Выбери опцию:',
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    reply_markup=weekdays_main_inline_student(call.data))
    elif call.data.split("_")[0] == "files":
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=others_inline())
        for file in await files.take_file(call.data.split("_")[-1]):
            if file[0]:
                await bot.send_document(chat_id=call.message.chat.id, document=file[0])
    elif call.data.split("_")[0] == "adminfiles":
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=admin_docs_inline())
        document_name = call.data.split("_")[-1]
        await files.delete_file(document_name)
        await call.message.answer(f"Документ {document_name} был удален.")

    elif call.data.split("_")[0] == "adminspam":
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=spamming_inline())
        group_name = call.data.split("_")[-1]
        await state.update_data(group_name=group_name)
        await state.set_state(Spam.text_group)
        await call.message.answer("Введите текст.")

    elif call.data.split("_")[0] == "adminaccounts":
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=redact_user_inline())
        login = call.data.split("_")[-1]
        await state.update_data(login=login)

    elif call.data in admin_offices:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data='admin_offices')]])

        name = admin_offices[call.data][0]
        cab = admin_offices[call.data][1]
        phone_number = admin_offices[call.data][2]
        email = admin_offices[call.data][3]
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    reply_markup=markup,
                                    text=f"{name}\n{cab}\n{phone_number}\n{email}")
    else:
        if len(call.data.split("_")) > 2:
            group_name = call.data.split("_")[0]
            group_callback = f'{call.data.split("_")[0]}_main'
            weekday = call.data.split("_")[-1]
        else:
            group_name = call.data.split("_")[0]
            group_callback = call.data.split("_")[0]
            weekday = call.data.split("_")[-1]
        if group_name in groups(schedule.get_group_count()):
            markup = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data=group_callback)]])
            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id, reply_markup=markup,
                                        text=f'<b><u>Расписание на {get_full_day_name(weekday)}</u></b>:\n{shedule_tuple_student(schedule.get_schedule_group(group_name, weekday))}',
                                        parse_mode="HTML")
        else:
            markup = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data=group_name)]])
            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id, reply_markup=markup,
                                        text=f'<b>Расписание на {get_full_day_name(weekday)}</b>:\n{shedule_tuple_teacher(schedule.get_schedule_teacher(group_name, weekday))}',
                                        parse_mode="HTML")
