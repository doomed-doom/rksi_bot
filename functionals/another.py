from aiogram.types import InlineKeyboardButton, KeyboardButton


def keyboard_chunks(lst):
    l = list()
    for i in lst:
        l.append(i[0])
    button = []
    buttons = []
    x = 0
    for i in l:
        x += 1
        button.append(KeyboardButton(text=i))
        if x == 3:
            x = 0
            buttons.append(button.copy())
            button.clear()
    buttons.append(button.copy())
    button.clear()
    return buttons


def inline_chunks(lst):
    l = list()
    for i in lst:
        l.append(i[0])
    button = []
    buttons = []
    x = 0
    for i in l:
        x += 1
        button.append(InlineKeyboardButton(text=i, callback_data=i))
        if x == 3:
            x = 0
            buttons.append(button.copy())
            button.clear()
    buttons.append(button.copy())
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data='Back')])
    button.clear()
    return buttons


def files_inline_chunks(lst):
    l = list()
    for i in lst:
        l.append(i[0])
    button = []
    buttons = []
    x = 0
    for i in l:
        x += 1
        button.append(InlineKeyboardButton(text=i, callback_data=f"files_{i}"))
        if x == 3:
            x = 0
            buttons.append(button.copy())
            button.clear()
    buttons.append(button.copy())
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data='others')])
    button.clear()
    return buttons


def admin_files_inline_chunks(lst):
    l = list()
    for i in lst:
        l.append(i[0])
    button = []
    buttons = []
    x = 0
    for i in l:
        x += 1
        button.append(InlineKeyboardButton(text=i, callback_data=f"adminfiles_{i}"))
        if x == 3:
            x = 0
            buttons.append(button.copy())
            button.clear()
    buttons.append(button.copy())
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data='files')])
    button.clear()
    return buttons


def admin_accounts_inline_chunks(lst):
    l = list()
    for i in lst:
        l.append(i[0])
    button = []
    buttons = []
    x = 0
    for i in l:
        x += 1
        button.append(InlineKeyboardButton(text=i, callback_data=f"adminaccounts_{i}"))
        if x == 3:
            x = 0
            buttons.append(button.copy())
            button.clear()
    buttons.append(button.copy())
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data='users')])
    button.clear()
    return buttons


def spam_inline_chunks(lst):
    l = list()
    for i in lst:
        l.append(i[0])
    button = []
    buttons = []
    x = 0
    for i in l:
        x += 1
        button.append(InlineKeyboardButton(text=i, callback_data=f"adminspam_{i}"))
        if x == 3:
            x = 0
            buttons.append(button.copy())
            button.clear()
    buttons.append(button.copy())
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data='spamming')])
    button.clear()
    return buttons


def shedule_tuple_student(lst):
    text = ""
    count = 0
    for l in lst:
        lesson = l[1]
        teacher = l[2]
        cabinet = l[4]
        count += 1
        text += f"{count}. {lesson}\n* Кабинет: {cabinet} корпус\n* Учитель: {teacher}\n \n"
    return text


def shedule_tuple_teacher(lst):
    text = ""
    count = 0
    for l in lst:
        lesson = l[1]
        group = l[0]
        cabinet = l[4]
        count += 1
        text += f"{count}. {lesson}\n* Кабинет: {cabinet} корпус\n* Группа: {group}\n \n"
    if not text:
        text = "Нету пар"
    return text


def groups(lst):
    l = list()
    for i in lst:
        l.append(i[0])
    return l


weekdays = {
    'ПН': 'Понедельник',
    'ВТ': 'Вторник',
    'СР': 'Среду',
    'ЧТ': 'Четверг',
    'ПТ': 'Пятницу',
    'СБ': 'Субботу',
}


def get_full_day_name(day):
    for k, v in weekdays.items():
        if k == day:
            return v
    return None


admin_offices = {
    "Директор": ["Сергей Николаевич Горбунов", "Каб. 203", "Тел: +7 (863) 206-88-88 доб. 2032", "rksi@rostobr.ru"],
    "Приемная Директора": ["Рыбальченко Татьяна Борисовна", "Каб. 216 (ул. Тургеневская, 10/6)",
                           "Тел: +7 (863) 206-88-88 доб. 2111", "rksi@rostobr.ru"],
    "Мед. пункт": ["Райф Татьяна Адольфовна", "Каб. 115 (ул. Тургеневская, 10/6)", "Тел: +7 (863) 206-88-88 доб. 1151",
                   ""],
    "Бухгалтерия": ["Оксана Марковна Немчицкая", "Каб. 108", "Тел: +7 (863) 206-88-88 доб. 1081", "glbux@adm.rksi.ru"],
    "Библиотека": ["Кривошеева Екатерина Ивановна", "Каб. 215 (ул. Тургеневская, 10/6)",
                   "Тел: +7 (863) 206-88-88 доб. 2151", "krivosheeva@adm.rksi.ru"],
}
