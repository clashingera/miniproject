import datetime
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(host='localhost', user='root', password='4349', database='expense_tracker')
cursor = db.cursor()

@app.route('/')
def index():
    # Fetch today's expenses from the database
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE date = %s", (today,))
    today_expense = cursor.fetchone()[0] or 0  # Set to 0 if there are no expenses today

    # Fetch this month's expenses from the database
    first_day_of_month = datetime.datetime.today().replace(day=1).strftime('%Y-%m-%d')
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE date >= %s", (first_day_of_month,))
    this_month_expense = cursor.fetchone()[0] or 0  # Set to 0 if there are no expenses this month

    # Fetch all expenses for the expense table
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    return render_template('index.html', today_expense=today_expense, this_month_expense=this_month_expense, expenses=expenses)

# ... (rest of your code) ...
@app.route('/edit/<int:expense_id>')
def edit(expense_id):
    cursor.execute("SELECT * FROM expenses WHERE id = %s", (expense_id,))
    expense = cursor.fetchone()
    return render_template('edit.html', expense=expense)

@app.route('/update/<int:expense_id>', methods=['POST'])
def update(expense_id):
    description = request.form['description']
    amount = float(request.form['amount'])
    category = request.form['category']
    date = request.form['date']

    sql = "UPDATE expenses SET description = %s, amount = %s, category = %s, date = %s WHERE id = %s"
    values = (description, amount, category, date, expense_id)
    cursor.execute(sql, values)
    db.commit()

    return redirect('/')



@app.route('/delete/<int:expense_id>')
def delete(expense_id):
    cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
    db.commit()
    return redirect('/')

@app.route('/add', methods=['POST'])
def add():
    description = request.form['description']
    amount = float(request.form['amount'])
    category = request.form['category']
    date = request.form['date']

    sql = "INSERT INTO expenses (description, amount, category, date) VALUES (%s, %s, %s, %s)"
    values = (description, amount, category, date)
    cursor.execute(sql, values)
    db.commit()

    return redirect('/')



@app.route('/this_month/<date>')
def this_month(date):
    month_start = f"{date[:7]}-01"
    month_end = f"{date[:7]}-31"  # Assuming all months have 31 days for simplicity

    cursor.execute("SELECT * FROM expenses WHERE date BETWEEN %s AND %s", (month_start, month_end))
    expenses = cursor.fetchall()
    return render_template('this_month.html', expenses=expenses)

# ... (previous imports and code) ...

# ... (previous imports and code) ...

# @app.route('/')
# def index():
#     # Fetch today's expenses from the database
#     today = datetime.datetime.today().strftime('%Y-%m-%d')
#     cursor.execute("SELECT SUM(amount) FROM expenses WHERE date = %s", (today,))
#     today_expense = cursor.fetchone()[0] or 0  # Set to 0 if there are no expenses today

#     # Fetch this month's expenses from the database
#     first_day_of_month = datetime.datetime.today().replace(day=1).strftime('%Y-%m-%d')
#     cursor.execute("SELECT SUM(amount) FROM expenses WHERE date >= %s", (first_day_of_month,))
#     this_month_expense = cursor.fetchone()[0] or 0  # Set to 0 if there are no expenses this month

#     # Fetch all expenses for the expense table
#     cursor.execute("SELECT * FROM expenses")
#     expenses = cursor.fetchall()

#     return render_template('index.html', today_expense=today_expense, this_month_expense=this_month_expense, expenses=expenses)

# ... (rest of your code) ...

# ... (rest of your code) ...








if __name__ == '__main__':
    app.run(debug=True)
# ... (previous imports and code) ...



