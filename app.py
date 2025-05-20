from flask import Flask, render_template, request, redirect, Response
from markupsafe import Markup
import sqlite3
import json

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']
        c.execute("INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
                  (amount, category, date))
        conn.commit()

    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    total = sum(exp[1] for exp in expenses)
    conn.close()
    return render_template('index.html', expenses=expenses, total=total, expenses_json=Markup(json.dumps(expenses)))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']
        c.execute("UPDATE expenses SET amount = ?, category = ?, date = ? WHERE id = ?",
                  (amount, category, date, id))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        c.execute("SELECT * FROM expenses WHERE id = ?", (id,))
        expense = c.fetchone()
        conn.close()
        return render_template('edit.html', expense=expense)

@app.route('/export')
def export_csv():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT amount, category, date FROM expenses")
    data = c.fetchall()
    conn.close()

    def generate():
        yield 'Amount,Category,Date\n'
        for row in data:
            yield f"{row[0]},{row[1]},{row[2]}\n"

    return Response(generate(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment; filename=expenses.csv"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
