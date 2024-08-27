"""
In my ORMish app this module holds the base classes for the core of the app.
The models inherit from the database class and use those methods to operate 
on the Budget and Expense object respectively.
"""


from database import Database
from datetime import datetime


###################################################################################################
# Base Classes
###################################################################################################

class Expense:
    """
    The Expense serves as the base class for the ExpenseModel and contains
    all of the desired information about a single expense. 
    """
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
    """
    The Budget serves as the base class for the BudgetModel and contains the
    budget month as well as each line item's budget. It also contains methods
    that work with the ExpenseModel to calculate the total, spent, and remaining
    for each line item.
    """
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
        """
        Sums all of the budget's line items for the total budget.
        """
        budgeted = {key: value for key, value in self.__dict__.items() if key != "budget_month"}
        budgeted["total"] = sum([value for value in budgeted.values()])
        return budgeted

    def __get_expenses(self):
        """
        Retrieves all of the expenses for the current budget's month.
        """
        model = ExpenseModel()
        return model.select_all(self.budget_month)

    def __calc_spent(self, expenses):
        """
        Sums the expenses for the given month by line item and then calculates
        the total spent.
        """
        spent = {key: 0 for key in self.__dict__.keys() if key != "budget_month"}
        for expense in expenses:
            spent[expense.line_item] += expense.amount
        spent["total"] = sum([value for value in spent.values()])
        return spent

    def __calc_remaning(self, budgeted, spent):
        """
        For each line item subtracts the amount in the spent dictionary from
        the budgeted dictionary. 
        """
        remaining = {}
        for key, value in budgeted.items():
            remaining[key] = value - spent[key]
        return remaining

    def calc_budget(self):
        """
        Calls all of the 'private' methods in the proper order and then returns
        a dictionary that summarzes the current state of the budget. 
        """
        budget_dict = self.__dict__
        budgeted = self.__calc_total()
        expenses = self.__get_expenses()
        spent = self.__calc_spent(expenses)
        remaining = self.__calc_remaning(budgeted, spent)
        return {"month": self.budget_month,
                "budgeted": budgeted,
                "expenses": expenses,
                "spent": spent,
                "remaining": remaining,
                "budget_dict": budget_dict}



###################################################################################################
# Model Classes
###################################################################################################


class BudgetModel(Database):
    """
    This model inherits from the Database class. In addition to the methods
    defined here, it uses the query, add, update, and delete from the parent
    class.
    """
    def __init__(self):
        """
        Inherits from the parent class and sets the fields for the table
        as all of the attributes from the Budget class.
        """
        super().__init__()
        self.table= "budgets"
        self.primary_key = "budget_month"
        self.fields = [key for key in Budget().__dict__.keys()]

    def create_table(self):
        """
        Creates the budgets table in the database by using the fields and
        adding the datatypes. 
        """
        columns = ["budget_month VARCHAR(7) PRIMARY KEY",]
        columns.extend([f"{field} SMALLINT UNSIGNED DEFAULT 0" for field in self.fields if field != "budget_month"])
        self.query(f"CREATE TABLE {self.table} ({", ".join(columns)});")
        

    def select_budget(self, budget_month):
        """
        Selects a row from the budgets table and then converts that row into 
        a Budget object.
        """
        results = self.select_row(key_value=budget_month)
        if results:
            return Budget(*results)
        else:
            return None
    
    def avaliable_budgets(self):
        return [result[0] for result in self.query(f"SELECT {self.primary_key} FROM {self.table}")]
    

class ExpenseModel(Database):
    """
    This model inherits from the Database class. In addition to the methods
    defined here, it uses the query, add, update, and delete from the parent
    class. It also has two more methods that the BudgetModel.
    """
    def __init__(self):
        """
        In additon to inhering from the parent class, the __init__ method
        sets the payment_methods and line_items lists that will serve as 
        ENUM values in the table. It also defines the fields for the table
        as the attributes of the Expense class.
        """
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
        self.line_items = [line_item for line_item in Budget().__dict__.keys() if line_item != "budget_month"]
        self.budget_months = [f"{i}-{datetime.now().year}" for i in range(1, 13)]

    def create_table(self):
        """
        Creates the expenses table in the database by using the fields and
        adding the datatypes. 
        """
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
        self.query(f"CREATE TABLE {self.table} ({", ".join(columns)});")

    def select_expense(self, expense_id):
        """
        Selects a row from the expenses table and converts it into an Expense
        object. 
        """
        results = self.select_row(key_value=expense_id)
        return Expense(*results)
    
    def select_all(self, budget_month, dictionary=False):
        """
        This method was created becuase it will be called frequently instead of constantly
        modifying the select_row or query methods.
        """
        results = self.query(f"SELECT * FROM {self.table} WHERE budget_month LIKE '{budget_month}';", dictionary=dictionary)
        return [Expense(*result) for result in results]
    
    def get_enums(self, field):
        """
        This method gets the ENUM values of the argument column so that they can
        be used in the HTML select box. 
        """
        return self.__dict__[field]

if __name__ == "__main__":
    """ Creates the database and tables for the app"""
    connection = Database(db_name=None)
    connection.query("CREATE DATABASE budget_app;")
    budget = BudgetModel()
    budget.create_table()
    expense = ExpenseModel()
    expense.create_table()

    # Sample Budgets
    for i in range(1, 13):
        budget = Budget(f"{i}-2024", 100, 100, 100, 100, 100, 100, 100, 100, 100)
        BudgetModel().add(budget)

    # Sample Expenses
    import random
    for i in range(1, 101):
        day = random.randint(1, 28)
        month = random.randint(1, 12)
        model = ExpenseModel()
        expense = Expense(i, f"sample {i}", random.randint(1, 50),
                          f"2024-{month}-{day}", f"merchant {i}",
                          random.choice(model.line_items),
                          random.choice(model.payment_methods),
                          f"{month}-2024")
        model.add(expense)