from flask import Flask, render_template, request, redirect, url_for
from models import Budget, Expense, BudgetModel, ExpenseModel
from datetime import datetime


def create_context(budget_month):
    current_budget = BudgetModel().select_budget(budget_month)
    if current_budget:
        budget_summary = current_budget.calc_budget()
        budget_summary["is_budget"] = True
    else:
        budget_summary = {"is_budget": False}
    budget_summary["months"] = BudgetModel().avaliable_budgets()
    budget_summary["current"] = budget_month
    budget_summary["line_items"] = ExpenseModel().line_items
    budget_summary["payment_methods"] = ExpenseModel().payment_methods
    return budget_summary


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """The inital page for the app. It uses the current date to generate all
    the tables' data."""
    return (render_template("index.html", context=create_context(datetime.now().strftime("%-m-%Y"))))

@app.route("/<budget_month>", methods=["GET"])
def home(budget_month):
    """
    This route serves as the home page for the app after any changes are made.
    It takes the budget_month passed from the other views and generates the data.
    """
    return render_template("index.html", context=create_context(budget_month))

@app.route("/month/<budget_month>", methods=["GET"])
@app.route("/month", methods=["POST"])
def month(budget_month=None):
    """
    This route allows the user to change the month to a different budget.
    """
    if request.method == "GET":
        return render_template("month.html", context=create_context(budget_month))
    elif request.method == "POST":
        return redirect(url_for("home", budget_month=request.form.get("chosen_month")))

    
@app.route("/delete", methods=["POST"])
def delete():
    """
    This route deletes an expense from the table and then returns to the home
    page which will update to include the current database table. 
    """
    expense = ExpenseModel().select_expense(request.form.get("expense_id"))
    ExpenseModel().delete(expense)
    return redirect(url_for("home", budget_month=expense.budget_month))

@app.route("/edit", methods=["POST"])
def edit():
    """
    This route uses the expense id to retrieve the expense and then
    render the edit.html form to make the changes. 
    """
    expense = ExpenseModel().select_expense(request.form.get("expense_id"))
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
    return redirect(url_for("home", budget_month=expense.budget_month))

@app.route("/add", methods=["POST"])    
@app.route("/add/<budget_month>", methods=["GET"])
def add(budget_month=None):
    """
    This route allows the user to add a new expense to the expenses table. 
    """
    if request.method == "GET":
        context=create_context(budget_month)
        context["current_date"] = datetime.now().strftime("%Y-%m-%d")
        context["expense"] = Expense()
        return render_template("add.html", context=context)

    elif request.method == "POST":
        data = request.form
        expense = Expense(*data.values())
        ExpenseModel().add(expense)
        return redirect(url_for("home", budget_month=expense.budget_month))

@app.route("/add_budget", methods=['GET', 'POST'])
def add_budget():
    """
    This route allows the use to create a new budget.
    """
    if request.method == "GET":
        context = create_context(datetime.now().strftime("%-m-%Y"))
        context["budget_fields"] = BudgetModel().fields
        context["months"] += [f"{i}-{datetime.now().year + 1}" for i in range(1, 13)]
        context["months"] += [f"{i}-{datetime.now().year - 1}" for i in range(1, 13)]
        return render_template("add_budget.html", context=context)
    elif request.method == "POST":
        data = request.form
        budget = Budget(*data.values())
        BudgetModel().add(budget)
        return redirect(url_for("home", budget_month=budget.budget_month))
    
@app.route("/edit_budget", methods=['POST'])
@app.route("/edit/<budget_month>", methods=['GET'])
def edit_budget(budget_month=None):
    if request.method == 'GET':
        context = create_context(budget_month)
        return render_template("edit_budget.html", context=context)
    elif request.method == 'POST':
        data = request.form.values()
        budget = Budget(*data)
        BudgetModel().update(budget)
        return redirect(url_for("home", budget_month=budget.budget_month))
    
@app.route("/delete_budget/<budget_month>", methods=["GET"])
def delete_budget(budget_month):
    budget = BudgetModel().select_budget(budget_month)
    BudgetModel().delete(budget)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()

##### make table bodys scrollable
#### add option to check emails for expenses to add
#### clearn up html and css
#### add ReadMe
### check submission validity before updating or adding ###
### testing
### logging