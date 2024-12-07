from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# SQLite database setup
DATABASE = 'Financetracker.db'


def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            income REAL NOT NULL,
            spent REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            payment_method TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()


init_db()


@app.route('/')
def index():
    if 'username' in session:
        user_id = session['user_id']
        username = session['username']

        # Fetch transactions from the database
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
        transactions = c.fetchall()

        # Compute the sum of transaction amounts for each payment method
        total_income = sum(transaction[2] for transaction in transactions)  # income (index 2)
        total_spent = sum(transaction[3] for transaction in transactions)  # spent (index 3)
        total_upi = sum(
            transaction[3] for transaction in transactions if transaction[7] == 'Online')  # spent for UPI (index 7)
        total_cash = sum(
            transaction[3] for transaction in transactions if transaction[7] == 'Cash')  # spent for Cash (index 7)

        conn.close()

        return render_template('index.html', username=username, total_spent=total_spent, total_income=total_income,
                               total_upi=total_upi, total_cash=total_cash)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]  # Store user_id in session
            session['username'] = user[1]  # Store username in session
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = c.fetchone()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            c.execute("INSERT INTO users (username, email, phone, password) VALUES (?, ?, ?, ?)",
                      (username, email, phone, password))
            conn.commit()
            conn.close()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('Signup.html')


@app.route('/transactions')
def transactions():
    if 'username' in session:
        user_id = session['user_id']  # Assuming you store user_id in session
        username = session['username']
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
        transactions = c.fetchall()
        conn.close()

        return render_template('transaction.html', transactions=transactions, username=username)
    else:
        return redirect(url_for('login'))


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if 'username' in session:
        user_id = session['user_id']  # Assuming you store user_id in session
        date = request.form['date']
        category = request.form['category']
        income = request.form['income']
        spent = request.form['spent']
        payment_method = request.form['payment_method']
        description = request.form['notes']

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(
            "INSERT INTO transactions (user_id, date, category, income, spent, payment_method, description) VALUES (?, ?, ?, ?, ?, ?, ?) ",
            (user_id, date, category, income, spent, payment_method, description))
        conn.commit()
        conn.close()

        return redirect(url_for('transactions'))
    else:
        return redirect(url_for('login'))


@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    if 'username' in session:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        conn.close()
        flash('Transaction deleted successfully.', 'success')
    else:
        flash('You must be logged in to delete a transaction.', 'error')
    return redirect(url_for('transactions'))


@app.route('/daily_spending_data')
def daily_spending_data():
    if 'username' in session:
        user_id = session['user_id']

        # Fetch daily spending data from the database
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT date, SUM(income), SUM(spent) FROM transactions WHERE user_id = ? GROUP BY date", (user_id,))
        data = c.fetchall()
        conn.close()

        # Format data for Chart.js
        labels = [row[0] for row in data]  # Date as labels
        spent = [row[1] for row in data]  # Total spent for each day
        income = [row[2] for row in data]  # Total income for each day

        return jsonify({'labels': labels, 'income': income, 'spent': spent})
    else:
        return redirect(url_for('login'))


@app.route('/monthly_spending_data')
def monthly_spending_data():
    if 'username' in session:
        user_id = session['user_id']

        # Fetch monthly spending data from the database
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(
            "SELECT strftime('%Y-%m', date) AS month, SUM(spent), SUM(income) FROM transactions WHERE user_id = ? GROUP BY month",
            (user_id,))
        data = c.fetchall()
        conn.close()

        # Format data for Chart.js
        labels = [datetime.strptime(row[0], '%Y-%m').strftime('%b %Y') for row in
                  data]  # Format month to display as 'Jan 2024'
        spent = [row[1] for row in data]  # Total spent for each month
        income = [row[2] for row in data]  # Total income for each month

        return jsonify({'labels': labels, 'income': income, 'spent': spent})
    else:
        return redirect(url_for('login'))

@app.route('/category_spending_data')
def category_spending_data():
    if 'username' in session:
        user_id = session['user_id']
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("""
            SELECT category, SUM(spent) as total_spent
            FROM transactions
            WHERE user_id = ?
            GROUP BY category
        """, (user_id,))
        data = c.fetchall()
        conn.close()

        labels = [row[0] for row in data]
        values = [row[1] for row in data]

        return jsonify({
            'labels': labels,
            'values': values
        })
    else:
        return redirect(url_for('login'))

# Assuming you have already set up your Flask app and database connection
@app.route('/income_vs_expenditure_data')
def income_vs_expenditure_data():
    if 'username' in session:
        user_id = session['user_id']
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        # Get total income
        c.execute("""
            SELECT SUM(income) as total_income
            FROM transactions
            WHERE user_id = ?
        """, (user_id,))
        total_income = c.fetchone()[0] or 0

        # Get total expenditure
        c.execute("""
            SELECT SUM(spent) as total_expenditure
            FROM transactions
            WHERE user_id = ?
        """, (user_id,))
        total_expenditure = c.fetchone()[0] or 0

        conn.close()

        return jsonify({
            'income': total_income,
            'spent': total_expenditure
        })
    else:
        return redirect(url_for('login'))

@app.route('/statistics')
def statistics():
    user_id = session.get('user_id')
    if user_id:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        c.execute("SELECT SUM(spent) FROM transactions WHERE user_id = ?", (user_id,))
        total_expenses_result = c.fetchone()
        total_expenses = total_expenses_result[0] if total_expenses_result and total_expenses_result[0] is not None else 0

        c.execute("SELECT category, SUM(income) as total_income, SUM(spent) as total_spent FROM transactions WHERE user_id = ? GROUP BY category", (user_id,))
        expense_by_category_result = c.fetchall()
        expense_by_category = {category: {"income": income, "spent": spent} for category, income, spent in expense_by_category_result} if expense_by_category_result else {}

        c.execute("SELECT category, SUM(spent) as total_spent FROM transactions WHERE user_id = ? GROUP BY category ORDER BY total_spent DESC LIMIT 5", (user_id,))
        top_spending_categories_result = c.fetchall()
        top_spending_categories = dict(top_spending_categories_result) if top_spending_categories_result else {}

        conn.close()

        return render_template('statistics.html', total_expenses=total_expenses, expense_by_category=expense_by_category, top_spending_categories=top_spending_categories)

    return redirect(url_for('login'))


@app.route('/edit_transaction/<int:transaction_id>', methods=['POST'])
def edit_transaction(transaction_id):
    # Extract form data
    date = request.form.get('date')
    category = request.form.get('category')
    income = request.form.get('income', 0)
    spent = request.form.get('spent', 0)
    payment_method = request.form.get('payment_method')
    notes = request.form.get('notes')

    if 'username' in session:
        user_id = session['user_id']
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        # Update the transaction in the database
        c.execute("""
            UPDATE transactions
            SET date = ?, category = ?, income = ?, spent = ?, payment_method = ?, description = ?
            WHERE id = ? AND user_id = ?
        """, (date, category, income, spent, payment_method, notes, transaction_id, user_id))

        conn.commit()
        conn.close()

    return redirect(url_for('transactions'))
if __name__ == '__main__':
    app.run(debug=True)
