import os

from flask import Flask, render_template, request,  url_for, redirect, flash, get_flashed_messages

# Import table definitions.
from models import *

app = Flask(__name__)

# Tell Flask what SQLAlchemy databas to use.
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:03561@localhost/expense'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)  
 
@app.route('/') #decorator drfines the   
def home():
    expenses = IncomeExpenses.query.all()  
    return render_template('index.html',expenses = expenses)

@app.route("/add", methods=['GET', 'POST'])  
def add():  
    if request.method == 'POST':
        amount = int(request.form.get("amount"))
        expense_type = request.form.get("Type")
        category = request.form.get("Category")
        incomeExpenses = IncomeExpenses(amount=amount,types=expense_type,category=category)
        db.session.add(incomeExpenses)
        db.session.commit()
        expenses = IncomeExpenses.query.all()  
        return render_template('index.html',expenses = expenses)
    else:
        return render_template('add.html')

@app.route('/delete/<int:entry_id>')
def delete(entry_id):
    expense = IncomeExpenses.query.get(int(entry_id))
    
    db.session.delete(expense)
    db.session.commit()
    expenses = IncomeExpenses.query.all()  
    return render_template('index.html',expenses = expenses)
@app.route('/dashboard')
def dashboard():
    expenses = IncomeExpenses.query.all()
    amount = []
    Type = ['Income','Outgoing']
    Category = ['Rent','Expense']
    income = 0
    outgoing = 0
    rent_amount = 0
    expense_amount = 0
    Category_amount = []
    for expense in expenses:
        if expense.types == 'Income':
            income += int(expense.amount)
        else:
            outgoing += int(expense.amount)
        
        if expense.category == 'Rent':
            rent_amount += expense.amount
        else:
            expense_amount += expense.amount
        
    

    amount.append(income)
    amount.append(outgoing)
    Category_amount.append(rent_amount)
    Category_amount.append(expense_amount)

    dates = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.date).group_by(IncomeExpenses.date).order_by(IncomeExpenses.date).all()
    print(dates)
    over_time_expenditure = []
    dates_labels = []
    for amo, date in dates:
        over_time_expenditure.append(amo)
        dates_labels.append(date.strftime("%d-%m-%Y"))
    return render_template('graph.html',amount = amount,Type = Type, Category_amount = Category_amount, Category = Category,over_time_expenditure=over_time_expenditure,dates_labels=dates_labels)
if __name__ =='__main__':  
    app.run(debug = True)  