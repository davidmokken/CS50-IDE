import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show transactions of stocks"""
    owned_shares = db.execute(f"SELECT symbol, name_share, \
    AVG(price) as average_bought_price, SUM(amount) as number_of_shares \
    FROM transactions WHERE id = :username GROUP BY symbol", username=session["user_id"])

    total_stocks_value = 0
    for owned_share in owned_shares:
        stock = lookup(owned_share["symbol"])
        owned_share["current_price"] = stock["price"]
        owned_share["holding_value"] = owned_share["current_price"]*owned_share["number_of_shares"]
        total_stocks_value += owned_share["holding_value"]

    current_cash = db.execute(f"SELECT cash FROM users WHERE id = :username", username=session["user_id"])
    current_cash = current_cash[0]["cash"]
    grand_total = total_stocks_value + current_cash
    return render_template("index.html", stocks=owned_shares, current_cash=current_cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # Validate the symbol
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Fill in an existing stock")

        # Validate the amount input
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Fill in an positive amount integer")

        shares = int(request.form.get("shares"))
        if not shares or shares <= 0:
            return apology("Fill in an positive amount of shares")

        # Look-up the current price for a stock and the cash of the user
        current_price = stock["price"]
        current_cash = db.execute(f"SELECT cash FROM users WHERE id = :username", username=session["user_id"])
        current_cash = current_cash[0]["cash"]

        # See if the user has valid funds for the purchase
        if current_cash < (current_price*shares):
            return apology("Invalid funds")

        # Insert the bought stock/shares into transactions
        else:
            db.execute("INSERT INTO transactions (id, symbol, name_share, price, amount, buy_sell) \
            VALUES(:id, :symbol, :name_share, :price, :amount, :buy_sell)",
                       id=session["user_id"], symbol=stock["symbol"], name_share=stock["name"],
                       price=stock["price"], amount=shares, buy_sell="Buy")

            # Update users cash
            current_cash = current_cash - (current_price*shares)
            db.execute(f"UPDATE users SET cash = :current_cash WHERE id = :name",
                       current_cash=current_cash, name=session["user_id"])
            return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    if request.method == "GET":

        # See if username does not appear in users
        username = request.args.get("username")
        if (len(username) != 0) and (len(db.execute("SELECT * FROM users WHERE \
        username = :username", username=username)) == 0):
            return jsonify(True)
        else:
            return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    owned_shares = db.execute(f"SELECT symbol, name_share, price, amount, date, buy_sell \
    FROM transactions WHERE id = :username", username=session["user_id"])

    return render_template("history.html", stocks=owned_shares)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Fill in an existing stock")
        else:
            return render_template("quoted.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation")

        # Ensure confirmation and password are the same
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("Password and confirmation password are not the same")

        # Register new user
        else:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                                  username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

            # If user is already registered return apology
            if not new_user:
                return apology("Username already taken.")

            # Start session and redirect to the homepage
            else:
                session["user_id"] = new_user
                return redirect("/")
    else:
        return render_template("register.html")


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add cash to wallet"""

    if request.method == "POST":

        amount = float(request.form.get("amount"))
        # Amount needs to be a positive amount
        if not amount or amount <= 0:
            return apology("Fill in a correct amount")
        db.execute("UPDATE users SET cash = cash + :amount WHERE id = username",
                   username=session["user_id"], amount=amount)
        return redirect("/")

    else:
        return render_template("addcash.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        stock = lookup(request.form.get("symbol"))
        shares = int(request.form.get("shares"))

        # Stock and input validation
        if not stock:
            return apology("Fill in an existing stock")

        elif not shares or shares <= 0:
            return apology("Fill in an positive amount of shares")

        # See if the user has enough stocks
        user_shares = db.execute("SELECT SUM(amount) as total_amount_shares FROM \
        transactions WHERE id = :username and symbol = :symbol GROUP BY symbol",
                                 username=session["user_id"], symbol=request.form.get("symbol"))

        if user_shares[0]["total_amount_shares"] < 1 or shares > user_shares[0]["total_amount_shares"]:
            return apology("Not enough shares in transactions")

        price = stock["price"]
        total_price = shares * price

        # Insert sold shares into transactions
        db.execute("INSERT INTO transactions (id, symbol, name_share, price, amount, buy_sell) \
        VALUES(:id, :symbol, :name_share, :price, :amount, :buy_sell)", id=session["user_id"],
                   symbol=stock["symbol"], name_share=stock["name"], price=price, amount=-shares, buy_sell="Sell")

        db.execute("UPDATE users SET cash = cash + :total_price WHERE id = :username",
                   username=session["user_id"], total_price=total_price)

        return redirect("/")

    else:
        # Show available stocks in the form
        owned_stocks = db.execute("SELECT symbol, SUM(amount) as total_amount_shares FROM transactions \
        WHERE id = :username GROUP BY symbol", username=session["user_id"])
        return render_template("sell.html", owned_stocks=owned_stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
