from datetime import datetime


class Budget:
    def __init__(self, budget_id=None, gas=0, food=0, mortgage=0, phone=0,
                 electric=0, internet=0, trash=0, child_care=0, insurance=0):
        self.budget_id = budget_id
        self.gas = gas
        self.food = food
        self.mortgage = mortgage
        self.phone = phone
        self.electric = electric
        self.internet = internet
        self.trash = trash
        self.child_care = child_care
        self.insurance = insurance
