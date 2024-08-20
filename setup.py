from database import Database
from budget import Budget
from datetime import datetime
from expense import Expenses


current_date = datetime.now()
budget_months = [f"{month}/{current_date.year}" for month in range(1, 13)]
payment_methods = ["Credit Card", "Debit Card", "Check", "Cash"]
budget = Budget()
line_items = [key for key in budget.__dict__.keys()]
connection = Database(db_name=None)


def create_database(db_name):
    connection.query(f"CREATE DATABASE {db_name};")
    connection.query(f"USE {db_name};")
    connection.db_name = db_name

def create_budgets_table():
    columns = [f"{item} SMALLINT UNSIGNED DEFAULT 0" for item in line_items if item != "budget_id"]
    budget_id = f"budget_id ENUM('{"', '".join(budget_months)}') PRIMARY KEY"
    create_statement = f"CREATE TABLE budgets ({budget_id}, {', '.join(columns)});"
    connection.query(create_statement)

def create_expenses_table():
    expense = Expenses()
    columns = []
    for column in expense.__dict__.keys():
        if column == "expense_id":
            datatype = "INT UNSIGNED PRIMARY KEY AUTO_INCREMENT"
        elif column in ("description", "merchant"):
            datatype = "VARCHAR(30)"
        elif column == "amount":
            datatype = "DECIMAL(6,2)"
        elif column == "date":
            datatype = "DATE"
        elif column == "line_item":
            datatype = f"ENUM('{"', '".join(line_items)}')"
        elif column == "payment_method":
            datatype = f"ENUM('{"', '".join(payment_methods)}')"
        elif column == "budget_id":
            datatype = f"ENUM('{"', '".join(budget_months)}')"
        columns.append(f"{column} {datatype}")
    columns.append("FOREIGN KEY (budget_id) REFERENCES budgets(budget_id)")
    connection.query(f"CREATE TABLE expenses ({", ".join(columns)});")



if __name__ == "__main__":
    create_database("budget_app")
    create_budgets_table()
    create_expenses_table()





