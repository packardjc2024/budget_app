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
        self.table = None
        self.primary_key = None

        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name
        )

    def query(self, sql_statement, dictionary=False):
        cursor = self.connection.cursor(dictionary=dictionary)
        cursor.execute(sql_statement)
        result = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return result
     
    def get_row(self, key_value):
        return self.query(f"select * from {self.table} where {self.primary_key} like '{key_value}';")[0]
    
    def add(self, object):
        columns = ", ".join([key for key in object.__dict__.keys()])
        values = "', '".join([str(value) for value in object.__dict__.values()])
        self.query(f"INSERT INTO {self.table} ({columns}) VALUES('{values}');")

    def update(self, object):
        updates = [f"{key} = {value}" for key, value in object.__dict__.items() if key != self.primary_key]
        update_statement =  f"""UPDATE {self.table}
        SET {", ".join(updates)} 
        WHERE {self.primary_key} LIKE '{object.__dict__[self.primary_key]}';"""
        self.query(update_statement)

    def delete(self, object):
        self.query(f"DELETE FROM {self.table} WHERE {self.primary_key} LIKE '{object.__dict__[self.primary_key]}';")


if __name__ == "__main__":
    pass
