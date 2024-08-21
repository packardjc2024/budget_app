from database import Database


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
    

if __name__ == "__main__":
    budget = BudgetModel()
    budget.create_table()

    
