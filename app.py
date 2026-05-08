from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# MySQL Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Rajan@06@localhost/banking_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize Database
db = SQLAlchemy(app)


# Account Table
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=False)


# Transaction Table
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    receiver = db.Column(db.String(100), nullable=True)


# Create Database Tables
with app.app_context():
    db.create_all()

    # Insert Initial Account Balance
    if Account.query.first() is None:
        account = Account(balance=10000)
        db.session.add(account)
        db.session.commit()


# Home Page
@app.route("/")
def home():
    account = Account.query.first()
    transactions = Transaction.query.all()

    return render_template(
        "index.html",
        balance=account.balance,
        transactions=transactions
    )


# Deposit Route
@app.route("/deposit", methods=["POST"])
def deposit():
    amount = int(request.form["amount"])

    account = Account.query.first()
    account.balance += amount

    transaction = Transaction(
        action="Deposit",
        amount=amount
    )

    db.session.add(transaction)
    db.session.commit()

    return redirect("/")


# Transfer Route
@app.route("/transfer", methods=["POST"])
def transfer():
    amount = int(request.form["amount"])
    receiver = request.form["receiver"]

    account = Account.query.first()

    if amount <= account.balance:
        account.balance -= amount

        transaction = Transaction(
            action="Transfer",
            amount=amount,
            receiver=receiver
        )

        db.session.add(transaction)
        db.session.commit()

    else:
        transaction = Transaction(
            action="Failed Transfer",
            amount=amount,
            receiver=receiver
        )

        db.session.add(transaction)
        db.session.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
