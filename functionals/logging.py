from functionals.db import DBConfig


class Student(DBConfig):
    def check_user_session(self, session_id):
        self.mycursor.execute(f'SELECT * FROM hakaton.users WHERE session_id = {session_id}')
        result = self.mycursor.fetchall()
        return result

    async def leave_user_session(self, session_id):  # изменяет сессию юзера в бд
        self.mycursor.execute(f"UPDATE hakaton.users SET session_id = 0 WHERE session_id = {session_id};")
        self.db.commit()

    async def delete_user_account(self, login, password, main_group, session_id):  # изменяет сессию юзера в бд
        self.mycursor.execute(
            f"SELECT * FROM hakaton.users  WHERE login = '{login}' and password = '{password}' and session_id = {session_id} and main_group = '{main_group}'")
        result = self.mycursor.fetchall()
        if result:
            self.mycursor.execute(
                f"DELETE FROM hakaton.users  WHERE login = '{login}' and password = '{password}' and session_id = {session_id} and main_group = '{main_group}'")
            self.db.commit()
            return result
        else:
            return result


student = Student()


class UnLogging(DBConfig):
    # регистрация
    def set_user_to_db(self, login, password, main_group, msg):  # добавление юзера в базу данных
        self.mycursor.execute(
            f'INSERT INTO users (login, password, account_status, main_group, session_id) VALUES ("{login}", "{password}", "student", "{main_group}", {msg.from_user.id})')
        self.db.commit()

    def get_alreadyindb(self, login):  # проверка на уже существующий акк в базе данных
        try:
            self.mycursor.execute(f'SELECT login FROM users WHERE login = "{login}"')
            result = self.mycursor.fetchone()[0]
            return result
        except Exception as exception:
            return None

    def get_validation(self, login, password):  # проверка пароля на длинну
        if len(password) >= 8:
            if login.isalnum() and password.isalnum():  # состоит ли строка из цифр или букв
                return True

    async def register(self, message, data):  # сама регистрация пользователя
        if len(data) > 1:  # проверка длинны массива (введён ли был пароль)
            if self.get_validation(data['login'], data['password']):
                result = self.get_alreadyindb(data['login'])
                if data['login'] == result:
                    await message.answer('Этот логин занят.')
                else:
                    self.set_user_to_db(data['login'], data['password'], data['main_group'], message)
                    await message.answer(f'Ваш аккаунт создан!')
            else:
                await message.answer('Не корректен логин или пароль.')
        else:
            await message.answer('Вы не указали пароль!')


unloging = UnLogging()


class Schedule(DBConfig):
    def get_group_count(self):
        self.mycursor.execute("SELECT DISTINCT group_name FROM hakaton.schedule")
        result = self.mycursor.fetchall()
        return result

    def get_teacher_count(self):
        self.mycursor.execute("SELECT DISTINCT teacher FROM hakaton.schedule")
        result = self.mycursor.fetchall()
        return result

    def get_schedule_teacher(self, teacher_name, day):
        self.mycursor.execute(f'SELECT * FROM hakaton.schedule WHERE teacher = "{teacher_name}" AND day = "{day}"')
        result = self.mycursor.fetchall()
        return result

    def get_schedule_group(self, group_name, day):
        self.mycursor.execute(f'SELECT * FROM hakaton.schedule WHERE group_name = "{group_name}" AND day = "{day}"')
        result = self.mycursor.fetchall()
        return result


schedule = Schedule()


class Logging(DBConfig):
    async def check_user(self, login, password):
        self.mycursor.execute(f'SELECT * FROM hakaton.users WHERE login = "{login}" AND password = "{password}"')
        result = self.mycursor.fetchall()
        return result

    async def update_user_session(self, session_id, login):  # изменяет сессию юзера в бд
        self.mycursor.execute(f"UPDATE hakaton.users SET session_id = {int(session_id)} WHERE login = '{login}';")
        self.db.commit()


logging = Logging()


class StartUser(DBConfig):
    async def add_user(self, user_id, role='member', username='None'):
        self.mycursor.execute(
            f"INSERT INTO hakaton.user (user_id, role, username) VALUES ({user_id}, '{role}', '{username}');")
        self.db.commit()

    async def find_user(self, username):
        self.mycursor.execute(f'SELECT * FROM hakaton.user WHERE username = "{username}";')
        result = self.mycursor.fetchall()
        if result:
            return result

    async def check_user(self, user_id, username='None'):
        self.mycursor.execute(f'SELECT * FROM hakaton.user WHERE user_id = {user_id};')
        if not self.mycursor.fetchall():
            await self.add_user(user_id, username=username)
        else:
            self.mycursor.execute(
                f"SELECT * FROM hakaton.user WHERE role = 'owner' AND user_id = {user_id} OR role = 'admin' AND user_id = {user_id};")
            result = self.mycursor.fetchall()
            if result:
                return result

    async def change_role(self, username, role):
        self.mycursor.execute(f"UPDATE hakaton.user SET role = '{role}' WHERE username = '{username}';")
        self.db.commit()

    def get_accounts_count(self):
        self.mycursor.execute("SELECT login FROM hakaton.users;")
        result = self.mycursor.fetchall()
        return result

    async def del_account(self, login):
        self.mycursor.execute(
            f"DELETE FROM hakaton.users WHERE login = '{login}';")
        self.db.commit()

    async def change_attribute(self, method, old_value, new_value):
        self.mycursor.execute(f"UPDATE hakaton.users SET {method} = '{new_value}' WHERE login = '{old_value}';")
        self.db.commit()


start_user = StartUser()


class SpamUser(DBConfig):
    async def spam_all(self):
        self.mycursor.execute(
            f"SELECT user_id FROM hakaton.user;")
        result = self.mycursor.fetchall()
        return result

    async def spam_group(self, group_name):
        self.mycursor.execute(
            f"SELECT session_id, main_group  FROM hakaton.users WHERE main_group = '{group_name}';")
        result = self.mycursor.fetchall()
        return result

    async def spam_user_all(self):
        self.mycursor.execute(
            f"SELECT session_id  FROM hakaton.users;")
        result = self.mycursor.fetchall()
        return result


spam_user = SpamUser()


class Files(DBConfig):
    async def add_file(self, file_id, file_name):
        self.mycursor.execute(
            f"INSERT INTO hakaton.documents (file_id, file_name) VALUES ('{file_id}', '{file_name}')")
        self.db.commit()

    async def delete_file(self, file_name):
        self.mycursor.execute(
            f"DELETE FROM hakaton.documents WHERE file_name = '{file_name}';")
        self.db.commit()

    def get_file_name(self):
        self.mycursor.execute("SELECT file_name FROM hakaton.documents")
        result = self.mycursor.fetchall()
        return result

    async def take_file(self, file_name):
        self.mycursor.execute(f"SELECT * FROM hakaton.documents WHERE file_name = '{file_name}'")
        result = self.mycursor.fetchall()
        return result


files = Files()
