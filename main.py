from flask import Flask, render_template, request, redirect, url_for
from models import Budget, Expense, BudgetModel, ExpenseModel
from datetime import datetime


def create_context(budget_month):
    current_budget = BudgetModel().select_budget(budget_month)
    budget_summary = current_budget.calc_budget()
    budget_summary["months"] = [f"{i}-{datetime.now().year}" for i in range(1, 13)]
    budget_summary["current"] = budget_month
    budget_summary["line_items"] = ExpenseModel().line_items
    budget_summary["payment_methods"] = ExpenseModel().payment_methods
    return budget_summary


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
@app.route("/<budget_month>", methods=["GET", "POST"])
def index(budget_month=datetime.now().strftime("%-m-%Y")):
    """
    This route serves as the home page for the app. When it first loads it uses
    datetime to get the current date and uses that month to serve as the default
    budget month. It then retrieves and displays the budget summary and the
    expenses for the budget.
    """    
    if request.method == "POST":
        budget_month = request.form.get("chosen_month")
    return render_template("index.html", context=create_context(budget_month))
    
@app.route("/delete", methods=["POST"])
def delete():
    """
    This route deletes an expense from the table and then returns to the home
    page which will update to include the current database table. 
    """
    id = request.form.get("expense_id")
    expense = ExpenseModel().select_expense(id)
    ExpenseModel().delete(expense)
    return redirect(url_for("index", budget_month=expense.budget_month))

@app.route("/edit", methods=["POST"])
def edit():
    """
    This route uses the expense id to retrieve the expense and then
    render the edit.html form to make the changes. 
    """
    id = request.form.get("expense_id")
    expense = ExpenseModel().select_expense(id)
    dictionary = create_context(expense.budget_month)
    dictionary["expense"] = expense
    return render_template("edit.html", context=dictionary)
    
@app.route("/update", methods = ["POST"])
def update():
    """
    This route takes the changes to the expense entered into the form and 
    updates the table before redirecting to the home page. 
    """
    data = request.form
    expense = Expense(*data.values())
    ExpenseModel().update(expense)
    return redirect(url_for("index", budget_month=expense.budget_month))
        
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        budget_month = ""
        return render_template("add.html", context=create_context(budget_month))

    elif request.method == "POST":
        budget_month = ""
        return redirect(url_for("index", budget_month=expense.budget_month))

#### Add Expense
##### make table bodys scrollable
#### add option to check emails for expenses to add
#### clearn up html and css

if __name__ == "__main__":
    app.run()