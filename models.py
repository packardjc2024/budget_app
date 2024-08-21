from database import Database
from datetime import datetime


###################################################################################################
# Base Classes
###################################################################################################

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


class Budget:
    def __init__(self, budget_month=None, gas=None, food=None, mortgage=None,
                 phone=None, electric=None, internet=None, trash=None,
                 child_care=None, insurance=None):
        self.budget_month = budget_month
        self.gas = gas
        self.food = food
        self.mortgage = mortgage
        self.phone = phone
        self.electric = electric
        self.internet = internet
        self.trash = trash
        self.child_care = child_care
        self.insurance = insurance

    def __calc_total(self):
        budgeted = {key: value for key, value in self.__dict__.items() if key != "budget_monthg"}
        budgeted["total"] = sum([value for value in budgeted.values()])
        return budgeted

    def __get_expenses(self):
        model = ExpenseModel()
        return model.get_all(self.budget_month)

    def __calc_spent(self, expenses):
        spent = {}
        for expense in expenses:
            spent[expense.line_item] += expense.amount
        return spent

    def __calc_remaning(self, budgeted, spent):
        remaining = {}
        for key, value in budgeted.items():
            remaining[key] = value - spent[key]
        return remaining

    def calc_budget(self):
        budgeted = self.__calc_total()
        expenses = self.__get_expenses()
        spent = self.__calc_spent(expenses)
        remaining = self.__calc_remaning(budgeted, spent)
        return {"budgeted": budgeted,
                "expenses": expenses,
                "spent": spent,
                "remaining": remaining,}



###################################################################################################
# Model Classes
###################################################################################################


class BudgetModel(Database):
    """Can also add with self.add(object) and update with self.update(object)"""
    def __init__(self):
        super().__init__()
        self.table= "budgets"
        self.primary_key = "budget_month"
        self.fields = [key for key in Budget().__dict__.keys()]

    def create_table(self):
        columns = ["budget_month VARCHAR(7)",]
        columns.extend([f"{field} SMALL INT UNSIGNED DEFAULT 0" for field in self.fields if field != "budget_month"])
        self.query(f"INSERT INTO {self.table} ({", ".join(columns)});")

    def get_budget(self, budget_month):
        results = self.get_row(key_value=budget_month)
        return Budget(*results)
    

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
        self.line_items = [line_item for line_item in Budget().__dict__.keys()]
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
    
    def get_all(self, budget_month, dictionary=False):
        results = self.query(f"SELECT * FROM {self.table} WHERE budget_month LIKE '{budget_month}';", dictionary=dictionary)
        return [Expense(*result) for result in results]
    
    def get_enums(self, field):
        return self.__dict__[field]

    

if __name__ == "__main__":
    # connection = Database(db_name=None)
    # connection.query("CREATE budget_app;")
    # budget = BudgetModel()
    # budget.create_table()
    # expense = ExpenseModel()
    # expense.create_table()
    pass
