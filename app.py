from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Dummy data (simulate banking)
balance = 10000
transactions = []

@app.route("/")
def home():
    return render_template("index.html", balance=balance, transactions=transactions)

@app.route("/transfer", methods=["POST"])
def transfer():
    global balance
    amount = int(request.form["amount"])
    receiver = request.form["receiver"]

    if amount <= balance:
        balance -= amount
        transactions.append(f"Sent ₹{amount} to {receiver}")
    else:
        transactions.append("Insufficient Balance")

    return redirect("/")

@app.route("/deposit", methods=["POST"])
def deposit():
    global balance
    amount = int(request.form["amount"])
    balance += amount
    transactions.append(f"Deposited ₹{amount}")
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
