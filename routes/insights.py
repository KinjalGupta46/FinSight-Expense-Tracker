from flask import Blueprint, render_template, session, redirect
from database import mysql

insights_bp = Blueprint("insights", __name__)


@insights_bp.route("/insights")
def insights():

    if "user_id" not in session:
        return redirect("/login")

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT monthly_income
        FROM users
        WHERE id=%s
    """, (session["user_id"],))

    income = float(cursor.fetchone()[0] or 0)

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE user_id=%s
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """, (session["user_id"],))

    categories = cursor.fetchall()

    cursor.execute("""
        SELECT IFNULL(SUM(amount),0)
        FROM expenses
        WHERE user_id=%s
    """, (session["user_id"],))

    expense = float(cursor.fetchone()[0] or 0)

    savings = income - expense

    highest = "None"
    highest_amount = 0

    if categories:
        highest = categories[0][0]
        highest_amount = float(categories[0][1])

    # ---------------- Alerts ----------------

    alerts = []

    if savings < income * 0.20:
        alerts.append({
            "title": "Low Savings",
            "message": "Increase your monthly savings."
        })

    if highest != "None":
        alerts.append({
            "title": "Top Expense",
            "message": f"{highest} is your highest spending category."
        })

    alerts_count = len(alerts)
    latest_alerts = alerts[:5]

    cursor.close()

    return render_template(

        "insights.html",

        income=income,
        expense=expense,
        savings=savings,
        highest=highest,
        highest_amount=highest_amount,
        categories=categories,

        alerts_count=alerts_count,
        latest_alerts=latest_alerts

    )