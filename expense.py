from database import Database
from budget import Budget
from datetime import datetime


class Expense:
    def __init__(self, expense_id=None, description=None, amount=None,
                 date=None, merchant=None, line_item=None,
                 payment_method=None, budget_month=None):
        self.expense_id = expense_id
        self.description = description
        self.amount = amount
        self.date = date
        self.merchant = merchant
        self.line_item = line_item
        self.payment_method = payment_method
        self.budget_month = budget_month


class ExpenseModel(Database):
    """Can also add with self.add(object) and update with self.update(object)"""
    def __init__(self):
        super().__init__()
        self.table = "expenses"
        self.primary_key = "expense_id"
        self.fields = [key for key in Expense().__dict__.keys()]
        self.payment_methods = [
            'Credit Card',
            'Debit Card',
            'Cash',
            'Check',
        ]
        self.line_items = [key for key in Budget().__dict__.keys() if key != "budget_month"]
        self.budget_months = [f"{i}/{datetime.now().year}" for i in range(1, 13)]

    def create_table(self):
        columns = []
        for field in self.fields:
            if field == "expense_id":
                datatype = "INT UNSIGNED PRIMARY KEY AUTO_INCREMENT"
            elif field in ("description", "merchant"):
                datatype = "VARCHAR(30)"
            elif field == "amount":
                datatype = "DECIMAL(6,2)"
            elif field == "date":
                datatype = "DATE"
            elif field == "line_item":
                datatype = f"ENUM('{"', '".join(self.line_items)}')"
            elif field == "payment_method":
                datatype = f"ENUM('{"', '".join(self.payment_methods)}')"
            elif field == "budget_month":
                datatype = f"ENUM('{"', '".join(self.budget_months)}')"
            columns.append(f"{field} {datatype}")
        self.query(f"INSERT INTO {self.table} ({", ".join(columns)});")

    def get_expense(self, expense_id):
        results = self.get_row(key_value=expense_id)
        return Expense(*results)
    

if __name__ == "__main__":
    test = ExpenseModel()
    # test.create_table()

