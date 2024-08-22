"""
This module serves as the MySQL engine for my app. I created my own type of
ORM by using mysql.connector. The Database class in this module serves as 
the connection to the database and has the CRUD methods that are inherited
by the models classes. The CRUD methods were created generic so that they can
be called by the child classes without having to be overwritten. This class
is only inherited and never directly called except to create the database in
the setup of the app.
"""


import os
import mysql.connector


class Database:
    def __init__(self, db_name="budget_app", user="root",
                 password=os.environ['mysql_login'],
                 host="localhost"):
        """
        The connection is initialized in the __init__ method so that an extra
        like of code doesn't have to be written every time a child class is 
        instantiated. The table and primary_key attributes are not used here,
        but are necessary for the methods that the child classes will use.
        """
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
        """
        This method serves as the SQL executer. It also commits all queries in
        case it is an CRUD statement.
        """
        cursor = self.connection.cursor(dictionary=dictionary)
        cursor.execute(sql_statement)
        result = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return result
     
    def select_row(self, key_value):
        """
        This method returns a row of data from the table. It is the only method
        that is not called directly by the child classes, but instead is called
        and then added to.
        """
        return self.query(f"select * from {self.table} where {self.primary_key} like '{key_value}';")[0]
    
    def add(self, object):
        """
        Adds a row to the table. Takes either a budget or expense object as the
        argument.
        """
        columns = ", ".join([key for key in object.__dict__.keys()])
        values = "', '".join([str(value) for value in object.__dict__.values()])
        self.query(f"INSERT INTO {self.table} ({columns}) VALUES('{values}');")

    def update(self, object):
        """
        Updates a row to the table. Takes either a budget or expense object as the
        argument. Updates every column except the primary key even if there are no
        changes to save having to add extra arguments and logic.
        """
        updates = [f"{key} = '{value}'" for key, value in object.__dict__.items() if key != self.primary_key]
        update_statement =  f"""UPDATE {self.table}
        SET {", ".join(updates)} 
        WHERE {self.primary_key} LIKE '{object.__dict__[self.primary_key]}';"""
        self.query(update_statement)

    def delete(self, object):
        """
        Deletes a row to the table. Takes either a budget or expense object as the
        argument.
        """
        self.query(f"DELETE FROM {self.table} WHERE {self.primary_key} LIKE '{object.__dict__[self.primary_key]}';")