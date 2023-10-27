from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from functionals.another import weekdays, inline_chunks, spam_inline_chunks, files_inline_chunks, \
    admin_files_inline_chunks, admin_accounts_inline_chunks
from functionals.logging import schedule, files, start_user


def welcome_inline(group_name):
    # Добавляет кнопки для сообщения(максимум на 1 длине может быть 3 штуки кнопок: [[1,2,3], [1,2], [1,2,3], [1]])
    buttons = [
        [InlineKeyboardButton(text="Ваше Расписание ⏰", callback_data=f'{group_name}_main')],
        [InlineKeyboardButton(text="Расписания Студентов 🧑‍🎓", callback_data='sheldure_student')],
        [InlineKeyboardButton(text="Расписание преподователей  🧑‍🏫", callback_data='sheldure_teacher')],
        [InlineKeyboardButton(text="Другое 📃", callback_data='others'),
         ]]
    # Возвращает разметку кнопок для сообщения после использования функции
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def student_inline():
    buttons = inline_chunks(schedule.get_group_count())
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def spamming_group_inline():
    buttons = spam_inline_chunks(schedule.get_group_count())
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def docs_group_inline():
    buttons = files_inline_chunks(files.get_file_name())
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_docs_group_inline():
    buttons = admin_files_inline_chunks(files.get_file_name())
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_accounts_inline():
    buttons = admin_accounts_inline_chunks(start_user.get_accounts_count())
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def teacher_inline():
    buttons = inline_chunks(schedule.get_teacher_count())
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_office_inline():
    buttons = [
        [InlineKeyboardButton(text="Директор", callback_data='Директор')],
        [InlineKeyboardButton(text="Приемная Директора", callback_data='Приемная Директора')],
        [InlineKeyboardButton(text="Мед. пункт", callback_data='Мед. пункт')],
        [InlineKeyboardButton(text="Бухгалтерия", callback_data='Бухгалтерия')],
        [InlineKeyboardButton(text="Библиотека", callback_data='Библиотека')],
        [InlineKeyboardButton(text="🔙 Назад", callback_data='others')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def true_links_inline():
    buttons = [
        [InlineKeyboardButton(text="Сайт РКСИ", web_app=WebAppInfo(url='https://rksi.ru'))],
        [InlineKeyboardButton(text="Контактные данные", web_app=WebAppInfo(url='https://www.rksi.ru/contacts'))],
        [InlineKeyboardButton(text="Перевыпустить пропуск", web_app=WebAppInfo(url='https://rksi.ru/access_control'))],
        [InlineKeyboardButton(text="Новости РКСИ", web_app=WebAppInfo(url='https://rksi.ru/news'))],
        [InlineKeyboardButton(text="Прием в РКСИ", web_app=WebAppInfo(url='https://www.rksi.ru/priem'))],
        [InlineKeyboardButton(text="Заказать Справку", web_app=WebAppInfo(url='https://www.rksi.ru/account/enquiry'))],
        [InlineKeyboardButton(text="🔙 Назад", callback_data='others')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def others_inline():
    buttons = [
        [InlineKeyboardButton(text="Административные отделения 🗄", callback_data='admin_offices')],
        [InlineKeyboardButton(text="Документы 📄", callback_data='docs')],
        [InlineKeyboardButton(text="Полезные ссылки 📋", callback_data='true_links')],
        [InlineKeyboardButton(text="🔙 Назад", callback_data='Back')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def weekdays_inline_teacher(teacher_name):
    buttons = []
    for weekday in weekdays:
        buttons.append([InlineKeyboardButton(text=weekday, callback_data=f'{teacher_name}_{weekday}')])

    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data='sheldure_teacher')])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def weekdays_inline_student(group_name):
    buttons = []
    for weekday in weekdays:
        buttons.append([InlineKeyboardButton(text=weekday, callback_data=f'{group_name}_{weekday}')])

    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data='sheldure_student')])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def weekdays_main_inline_student(group_name):
    buttons = []
    for weekday in weekdays:
        buttons.append([InlineKeyboardButton(text=weekday, callback_data=f'{group_name}_{weekday}')])

    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data='Back')])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_panel_inline():
    buttons = [
        [InlineKeyboardButton(text="Устроить рассылку 📬", callback_data='spamming')],
        [InlineKeyboardButton(text="Работа с файлами 📑", callback_data='files')],
        [InlineKeyboardButton(text="Работа с пользователями 🙎🏼‍♂️", callback_data='users'),
         ]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_docs_inline():
    buttons = [
        [InlineKeyboardButton(text="Добавить файл 📥", callback_data='add_docs')],
        [InlineKeyboardButton(text="Удалить файл  📤️", callback_data='del_docs')],
        [InlineKeyboardButton(text="🔙 Назад", callback_data='admin_back')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def spamming_inline():
    buttons = [
        [InlineKeyboardButton(text="Написать всем 📬", callback_data='spamming_all')],
        [InlineKeyboardButton(text="Написать группе 📮", callback_data='spamming_group')],
        [InlineKeyboardButton(text="Написать зарегестрированным 👩🏼‍💼", callback_data='spamming_users')],
        [InlineKeyboardButton(text="🔙 Назад", callback_data='admin_back')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def users_redact_inline():
    buttons = [
        [InlineKeyboardButton(text="Редактирование учетной записи 👨🏼‍🎓", callback_data='redact_account')],
        [InlineKeyboardButton(text="Изменить роль 👩🏼‍✈️", callback_data='redact_role')],
        [InlineKeyboardButton(text="🔙 Назад", callback_data='admin_back')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def user_role_inline():
    buttons = [
        [InlineKeyboardButton(text="Сделать админом ⏫", callback_data='role_admin')],
        [InlineKeyboardButton(text="Сделать участником ⏬", callback_data='role_member')],
        [InlineKeyboardButton(text="🔙 Отмена", callback_data='cancel_role')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def redact_user_inline():
    buttons = [
        [InlineKeyboardButton(text="Изменить логин", callback_data='login_change')],
        [InlineKeyboardButton(text="Изменить пароль", callback_data='password_change')],
        [InlineKeyboardButton(text="Изменить группу", callback_data='group_change')],
        [InlineKeyboardButton(text="Удалить аккаунт", callback_data='account_delete')],
        [InlineKeyboardButton(text="Выйти с устройства", callback_data='session_change')],
        [InlineKeyboardButton(text="🔙 Отмена", callback_data='redact_account')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
