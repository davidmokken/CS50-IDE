import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")

# Writes answers of form to a sheet and a excel
# When one of the boxes is not filled in, the error.html is shown


@app.route("/form", methods=["POST"])
def post_form():
    first_name = request.form.get("firstname")
    last_name = request.form.get("lastname")
    age = request.form.get("age")
    gender = request.form.get("gender")
    email = request.form.get("email")
    city = request.form.get("city")
    born_city = request.form.get("borncity")
    favorite_club = request.form.get("favoriteclub")
    if not first_name or not last_name or not gender or not email or not city or not born_city or not favorite_club:
        return render_template("error.html")
    with open("survey.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow((first_name, last_name, age, gender, email, city, born_city, favorite_club))
    return redirect("/sheet")

# Shows sheet with all filled-in forms


@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open("survey.csv", "r") as file:
        reader = csv.reader(file)
        participants = list(reader)
    return render_template("sheet.html", participants=participants)
