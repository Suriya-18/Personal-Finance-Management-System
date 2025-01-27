from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY, type TEXT, amount REAL, description TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM transactions")
    transactions = c.fetchall()
    conn.close()
    return render_template('index.html', transactions=transactions)

@app.route('/add', methods=['POST'])
def add_transaction():
    type = request.form['type']
    amount = float(request.form['amount'])
    description = request.form['description']
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("INSERT INTO transactions (type, amount, description) VALUES (?, ?, ?)", (type, amount, description))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
