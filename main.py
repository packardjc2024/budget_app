from flask import Flask, render_template, request, redirect, url_for
from expense import Expense
from budget import Budget
from database import Database
from datetime import datetime


connection = Database()
current_date = datetime.now()
current_budget_month = current_date.strftime("%m/%Y")
current_budget = connection.select("budgets", f"budget_month like '{current_budget_month}'")
expense_columns, expense_displays = connection.columns("expenses")


app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home(request):
    if request.method == "GET":
        expenses = connection.select("expenses", {"budget_month": current_budget_month})
        context = {"expenses": expenses, "budget": current_budget, "current_budget_month": current_budget_month,
                "columns": expense_columns, "column_display_names": expense_displays}
        return render_template("home.html", context=context)






if __name__ == "__main__":
    app.run()