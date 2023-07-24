import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    id = session["user_id"]
    stocks = db.execute("SELECT symbol,price,sum(shares) as sum_shares FROM orders WHERE user_id = ? GROUP BY symbol;",id)
    cash = round(db.execute("SELECT cash FROM users WHERE id = ?",id)[0]["cash"],2)
    return render_template("index.html",stocks=stocks,cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        id = session["user_id"]
        symbol = request.form.get("symbol")
        shares = float(request.form.get("shares"))
        if not symbol  or not float.is_integer(shares) or shares <= 0:
            return apology("INVALID INPUT")
        stock = lookup(symbol)
        if not stock:
            return apology("NOT FOUND")
        cash = db.execute("SELECT cash FROM users WHERE id = ?;",id)[0]["cash"]
        balance = cash - stock["price"]*shares
        if balance < 0:
            return apology("NOT ENOUGH MONEY")
        db.execute("UPDATE users SET cash = ? WHERE id = ?;",balance,id)
        db.execute("INSERT INTO orders(user_id,symbol,shares,price) VALUES(?,?,?,?)",id,symbol,shares,stock["price"])
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    id = session["user_id"]
    stocks = db.execute("SELECT * FROM orders WHERE user_id = ?",id)
    return render_template("history.html",stocks = stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        name = request.form.get("stock_name")
        if not name:
            return apology("missing symbol")
        stock = lookup(name)
        if not stock:
            return apology("invalid symbol")
        return render_template("quote.html",stock = stock,method = request.method)
    else:
        return render_template("quote.html",method = request.method)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username or not password:
            return apology("please!")
        if db.execute("SELECT * FROM users WHERE username = ?;",username):
            return apology("used username")
        if password != confirmation:
            return apology("confirm")
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, hash)
        session["user_id"] = db.execute(
            "SELECT id FROM users WHERE username = ?;", username
        )[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    id = session["user_id"]
    stocks = db.execute("SELECT * FROM orders WHERE user_id = ? GROUP BY symbol;",id)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol")
        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol")
        shares = float(request.form.get("shares"))
        if not float.is_integer(shares):
            return apology("invalid shares")
        store = db.execute("SELECT sum(shares) as sum_shares FROM orders WHERE user_id = ? AND symbol = ? GROUP BY symbol ",id,symbol)[0]["sum_shares"]
        if store < shares:
            return apology("not enough shares")
        cash = db.execute("SELECT cash FROM users WHERE id = ?",id)[0]["cash"]
        money = stock["price"]*shares
        balance = cash + money
        if balance < 0:
            return apology("NOT ENOUGH money!")
        db.execute("UPDATE users SET cash = ? WHERE id = ?;",balance,id)
        db.execute("INSERT INTO orders(user_id,symbol,shares,price) VALUES(?,?,?,?)",id,symbol,-shares,stock["price"])
        return redirect("/")
    else:
        return  render_template("sell.html",stocks = stocks)
