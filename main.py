from flask import Flask, render_template, request, redirect, url_for
from expense import Expense, ExpenseModel
from budget import Budget, BudgetModel
from datetime import datetime

budget_model = BudgetModel()
expense_model = ExpenseModel()
current_date = datetime.now()
current_budget_month = current_date.strftime("%-m/%Y")
print(current_budget_month)
current_budget = budget_model.get_budget(current_budget_month)
expense_columns = expense_model.get_columns()
expense_displays = expense_model.get_display_columns()


app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        expenses = expense_model.get_all(current_budget_month)
        context = {"expenses": expenses,
                   "current_budget": current_budget,
                   "current_budget_month": current_budget_month,
                   "columns": expense_columns,
                   "column_display_names": expense_displays}
        return render_template("home.html", context=context)


###### work on budget class/model for calc totals
###### display those calculated totals on home page
##### clear up table where headers arent lined up with rows



if __name__ == "__main__":
    app.run()