from flask import Flask, render_template, request, redirect, url_for
from models import Budget, Expense, BudgetModel, ExpenseModel
from datetime import datetime


app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    current_date = datetime.now()
    current_budget_month = current_date.strftime("%-m/%Y")
    budget_model = BudgetModel()
    expense_model = ExpenseModel()

    if request.method == "GET":
        current_budget = budget_model.get_budget(current_budget_month)
        budget_summary = current_budget.calc_budget()
        return render_template("index.html", context=budget_summary)


###### display those calculated totals on home page
##### clear up table where headers arent lined up with rows



if __name__ == "__main__":
    app.run()