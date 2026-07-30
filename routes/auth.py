from flask import Blueprint, render_template, request, redirect, session, url_for
from database import mysql
import bcrypt
import re

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        monthly_income = request.form["monthly_income"]
        income_source = request.form["income_source"]
        financial_preference = request.form["financial_preference"]

        hashed_password = bcrypt.hashpw(
    password.encode("utf-8"),
    bcrypt.gensalt()
).decode("utf-8")

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            INSERT INTO users
            (full_name,email,phone,password,
            monthly_income,income_source,
            financial_preference)

            VALUES(%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                full_name,
                email,
                phone,
                hashed_password,
                monthly_income,
                income_source,
                financial_preference,
            ),
        )

        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT id,full_name,password,role FROM users WHERE email=%s",
            (email,),
        )

        user = cursor.fetchone()

        cursor.close()

        if user:

           if bcrypt.checkpw(
    password.encode("utf-8"),
    user[2].encode("utf-8")
):

                session["user_id"] = user[0]
                session["user_name"] = user[1]
                session["role"] = user[3]

                return redirect(url_for("dashboard.dashboard"))

        return "Invalid Email or Password"

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth_bp.login"))