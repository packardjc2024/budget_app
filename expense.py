


class Expenses:
    def __init__(self, expense_id=None, description=None, amount=None,
                 date=None, merchant=None, line_item=None,
                 payment_method=None, budget_id=None):
        self.expense_id = expense_id
        self.description = description
        self.amount = amount
        self.date = date
        self.merchant = merchant
        self.line_item = line_item
        self.payment_method = payment_method
        self.budget_id = budget_id
