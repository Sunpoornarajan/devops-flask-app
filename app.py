from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# -----------------------
# 🔹 DATABASE FUNCTIONS
# -----------------------
def get_db():
    return sqlite3.connect("bank.db")

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS account (
        id INTEGER PRIMARY KEY,
        balance INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT
    )
    """)

    cur.execute("INSERT OR IGNORE INTO account (id, balance) VALUES (1, 0)")

    conn.commit()
    conn.close()

init_db()


# -----------------------
# 🔹 ROUTES (PUT HERE)
# -----------------------

@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT balance FROM account WHERE id=1")
    balance = cur.fetchone()[0]

    cur.execute("SELECT message FROM transactions ORDER BY id DESC")
    transactions = [row[0] for row in cur.fetchall()]

    conn.close()
    return render_template("index.html", balance=balance, transactions=transactions)


@app.route("/deposit", methods=["POST"])
def deposit():
    amount = int(request.form["amount"])

    conn = get_db()
    cur = conn.cursor()

    cur.execute("UPDATE account SET balance = balance + ?", (amount,))
    cur.execute("INSERT INTO transactions(message) VALUES (?)",
                (f"Deposited ₹{amount}",))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/transfer", methods=["POST"])
def transfer():
    receiver = request.form["receiver"]
    amount = int(request.form["amount"])

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT balance FROM account WHERE id=1")
    balance = cur.fetchone()[0]

    if balance >= amount:
        cur.execute("UPDATE account SET balance = balance - ?", (amount,))
        cur.execute("INSERT INTO transactions(message) VALUES (?)",
                    (f"Sent ₹{amount} to {receiver}",))
    else:
        cur.execute("INSERT INTO transactions(message) VALUES (?)",
                    ("❌ Insufficient Balance",))

    conn.commit()
    conn.close()

    return redirect("/")


# -----------------------
# 🔹 RUN APP (BOTTOM)
# -----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
