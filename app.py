from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bank.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# -------------------------
# Database Models
# -------------------------

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=False)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    receiver = db.Column(db.String(100), nullable=True)


# -------------------------
# Create Database
# -------------------------

with app.app_context():
    db.create_all()

    if Account.query.first() is None:
        account = Account(balance=10000)
        db.session.add(account)
        db.session.commit()


# -------------------------
# Routes
# -------------------------

@app.route("/")
def home():
    account = Account.query.first()
    transactions = Transaction.query.order_by(Transaction.id.desc()).all()

    return render_template(
        "index.html",
        balance=account.balance,
        transactions=transactions
    )


@app.route("/deposit", methods=["POST"])
def deposit():
    amount = int(request.form["amount"])

    account = Account.query.first()
    account.balance += amount

    transaction = Transaction(
        action="Deposit",
        amount=amount,
        receiver=""
    )

    db.session.add(transaction)
    db.session.commit()

    return redirect("/")


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

    else:
        transaction = Transaction(
            action="Failed Transfer",
            amount=amount,
            receiver=receiver
        )

    db.session.add(transaction)
    db.session.commit()

    return redirect("/")


# -------------------------
# Run App
# -------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
