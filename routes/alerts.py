from flask import Blueprint, render_template, session, redirect
from database import mysql

alerts_bp = Blueprint("alerts", __name__)


@alerts_bp.route("/alerts")
def alerts():

    if "user_id" not in session:
        return redirect("/login")

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT monthly_income
        FROM users
        WHERE id=%s
    """,(session["user_id"],))

    income=float(cursor.fetchone()[0] or 0)

    cursor.execute("""
        SELECT IFNULL(SUM(amount),0)
        FROM expenses
        WHERE user_id=%s
    """,(session["user_id"],))

    expense=float(cursor.fetchone()[0] or 0)

    savings=income-expense

    cursor.execute("""
        SELECT category,SUM(amount)

        FROM expenses

        WHERE user_id=%s

        GROUP BY category

        ORDER BY SUM(amount) DESC
    """,(session["user_id"],))

    categories=cursor.fetchall()

    highest_category="None"

    if categories:
        highest_category=categories[0][0]

    alerts=[]

    if expense>income:

        alerts.append({

            "type":"danger",

            "title":"Budget Exceeded",

            "message":"Your expenses are higher than your monthly income."

        })

    elif expense>income*0.80:

        alerts.append({

            "type":"warning",

            "title":"Budget Warning",

            "message":"You have already used more than 80% of your income."

        })

    if savings<income*0.20:

        alerts.append({

            "type":"warning",

            "title":"Low Savings",

            "message":"Your savings are below the recommended 20%."

        })

    if highest_category!="None":

        alerts.append({

            "type":"info",

            "title":"Highest Spending Category",

            "message":f"You spent the most on {highest_category}."

        })

    if savings>=income*0.30:

        alerts.append({

            "type":"success",

            "title":"Excellent",

            "message":"Amazing! You are saving more than 30% of your income."

        })

    cursor.close()

    return render_template(

        "alerts.html",

        alerts=alerts

    )