from flask import Flask, render_template, request, redirect, url_for
from models import Budget, Expense, BudgetModel, ExpenseModel
from datetime import datetime


app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    """
    This route serves as the home page for the app. When it first loads it uses
    datetime to get the current date and uses that month to serve as the default
    budget month. It then retrieves and displays the budget summary and the
    expenses for the budget.
    """
    current_date = datetime.now()
    current_budget_month = current_date.strftime("%-m/%Y")
    budget_model = BudgetModel()
    expense_model = ExpenseModel()

    if request.method == "GET":
        current_budget = budget_model.select_budget(current_budget_month)
        budget_summary = current_budget.calc_budget()
        return render_template("index.html", context=budget_summary)


### continue finishing docs on models and on main
##### make table bodys scrollable
#### change budget month as the post to home



if __name__ == "__main__":
    app.run()