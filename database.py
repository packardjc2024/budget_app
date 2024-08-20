import os
import mysql.connector


class Database:
    def __init__(self, db_name="budget_app", user="root",
                 password=os.environ['mysql_login'],
                 host="localhost"):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host

        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name
        )

    def query(self, sql_statement):
        cursor = self.connection.cursor()
        cursor.execute(sql_statement)
        result = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return result