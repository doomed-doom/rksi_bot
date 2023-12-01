import mysql.connector


class DBConfig():
    def __init__(self):
        self.db = mysql.connector.connect(
            database='hakaton',
            user='root',
            password='root',
            host='localhost',
            port='3306',
            autocommit=True
        )
        self.mycursor = self.db.cursor()
