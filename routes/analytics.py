from flask import Blueprint, render_template, session, redirect
from database import mysql

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics")
def analytics():

    # ================= Login Check ================= #

    if "user_id" not in session:
        return redirect("/login")

    cursor = mysql.connection.cursor()

    # ================= Income ================= #

    cursor.execute("""
        SELECT monthly_income
        FROM users
        WHERE id=%s
    """, (session["user_id"],))

    user = cursor.fetchone()
    income = float(user[0]) if user and user[0] else 0

    # ================= Total Expense ================= #

    cursor.execute("""
        SELECT IFNULL(SUM(amount), 0)
        FROM expenses
        WHERE user_id=%s
    """, (session["user_id"],))

    total_expense = float(cursor.fetchone()[0] or 0)

    # ================= Savings ================= #

    savings = income - total_expense

    # ================= Budget Used (%) ================= #

    if income > 0:
        budget = round((total_expense / income) * 100)
    else:
        budget = 0

    # ================= Category Wise Expenses ================= #

    cursor.execute("""
        SELECT
            category,
            SUM(amount)
        FROM expenses
        WHERE user_id=%s
        GROUP BY category
    """, (session["user_id"],))

    category_data = cursor.fetchall()

    labels = []
    values = []

    for row in category_data:
        labels.append(row[0])
        values.append(float(row[1]))

    # ================= Monthly Expense Trend ================= #

    cursor.execute("""
        SELECT
            MONTH(expense_date),
            SUM(amount)
        FROM expenses
        WHERE user_id=%s
        GROUP BY MONTH(expense_date)
        ORDER BY MONTH(expense_date)
    """, (session["user_id"],))

    trend = cursor.fetchall()

    month_name = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }

    months = []
    month_expenses = []

    for row in trend:
        months.append(month_name.get(row[0], ""))
        month_expenses.append(float(row[1]))
        # ================= Spending Pattern Analysis ================= #

    highest_category = "None"
    highest_amount = 0

    if category_data:
        highest = max(category_data, key=lambda x: x[1])
        highest_category = highest[0]
        highest_amount = float(highest[1])

    total_category_expense = sum(values)

    food_percent = 0
    travel_percent = 0
    shopping_percent = 0

    for row in category_data:

        category = row[0].lower()
        amount = float(row[1])

        if total_category_expense > 0:
            percent = round((amount / total_category_expense) * 100)
        else:
            percent = 0

        if "food" in category:
            food_percent = percent

        elif "travel" in category:
            travel_percent = percent

        elif "shopping" in category:
            shopping_percent = percent

    # ================= Smart Budget Recommendation Engine ================= #

    recommendations = []

    # Budget Recommendation
    if budget >= 90:
        recommendations.append(
            "⚠️ You have almost exhausted your monthly budget."
        )

    elif budget >= 75:
        recommendations.append(
            "Reduce unnecessary expenses to stay within budget."
        )

    else:
        recommendations.append(
            "Great! Your spending is under control."
        )

    # Savings Recommendation
    if income > 0:

        if savings < income * 0.20:
            recommendations.append(
                "Increase your monthly savings to at least 20% of your income."
            )

        else:
            recommendations.append(
                "Excellent savings habit. Keep it up!"
            )

    # Category Recommendation
    if highest_category.lower() == "food":

        recommendations.append(
            "Food expenses are high. Consider reducing restaurant spending."
        )

    elif highest_category.lower() == "shopping":

        recommendations.append(
            "Shopping is your biggest expense. Avoid impulse purchases."
        )

    elif highest_category.lower() == "travel":

        recommendations.append(
            "Travel costs are high. Plan trips in advance to save money."
        )

    else:

        recommendations.append(
            f"Monitor your spending in '{highest_category}' category."
        )

    # ================= Financial Health Score ================= #

    health_score = 100

    if budget > 100:
        health_score -= 30

    elif budget > 80:
        health_score -= 15

    if income > 0 and savings < income * 0.20:
        health_score -= 20

    if highest_category.lower() in ["shopping", "food"]:
        health_score -= 10

    if health_score < 0:
        health_score = 0

    if health_score >= 90:
        health_status = "Excellent"

    elif health_score >= 75:
        health_status = "Good"

    elif health_score >= 60:
        health_status = "Average"

    elif health_score >= 40:
        health_status = "Poor"

    else:
        health_status = "Critical"
    
        # ================= Alert & Notification System ================= #

    alerts = []

    # Budget Alerts
    if budget >= 100:
        alerts.append({
            "type": "danger",
            "icon": "bi-exclamation-triangle-fill",
            "message": "Your monthly budget has been exceeded."
        })

    elif budget >= 80:
        alerts.append({
            "type": "warning",
            "icon": "bi-exclamation-circle-fill",
            "message": "You have used more than 80% of your budget."
        })

    # Savings Alerts
    if savings <= 0:
        alerts.append({
            "type": "danger",
            "icon": "bi-wallet2",
            "message": "Your expenses are higher than your income."
        })

    elif income > 0 and savings < income * 0.20:
        alerts.append({
            "type": "warning",
            "icon": "bi-piggy-bank",
            "message": "Your savings are below the recommended 20%."
        })

    # Highest Spending Category Alerts
    if highest_category.lower() == "shopping":
        alerts.append({
            "type": "info",
            "icon": "bi-bag-fill",
            "message": "Shopping is your highest spending category."
        })

    elif highest_category.lower() == "food":
        alerts.append({
            "type": "info",
            "icon": "bi-cup-hot-fill",
            "message": "Food expenses are the highest this month."
        })

    elif highest_category.lower() == "travel":
        alerts.append({
            "type": "info",
            "icon": "bi-airplane-fill",
            "message": "Travel expenses dominate your monthly spending."
        })

    # Financial Health Alert
    if health_score >= 90:
        alerts.append({
            "type": "success",
            "icon": "bi-check-circle-fill",
            "message": "Excellent financial health. Keep it up!"
        })

    elif health_score >= 75:
        alerts.append({
            "type": "success",
            "icon": "bi-emoji-smile-fill",
            "message": "Your financial health is good."
        })

    elif health_score >= 60:
        alerts.append({
            "type": "warning",
            "icon": "bi-emoji-neutral-fill",
            "message": "Your financial health is average. Try to save more."
        })

    else:
        alerts.append({
            "type": "danger",
            "icon": "bi-emoji-frown-fill",
            "message": "Your financial health needs improvement."
        })
    # ================= Save Notifications =================

    notify_cursor = mysql.connection.cursor()

    for alert in alerts:

            notify_cursor.execute("""
        SELECT id
        FROM notifications
        WHERE user_id=%s
        AND title=%s
        AND message=%s
        AND is_read=0
    """, (
        session["user_id"],
        "Financial Alert",
        alert["message"]
    ))

    exists = notify_cursor.fetchone()

    if not exists:

            notify_cursor.execute("""
            INSERT INTO notifications
            (user_id, title, message, type)
            VALUES (%s,%s,%s,%s)
        """, (
            session["user_id"],
            "Financial Alert",
            alert["message"],
            alert["type"]
        ))

    mysql.connection.commit()

    notify_cursor.close()
    # ================= Close Cursor ================= #

    cursor.close()

    # ================= Render Analytics ================= #
    alerts_count = len(alerts)

    latest_alerts = alerts[:5]
    return render_template(
        "analytics.html",

        # Summary Cards
        income=income,
        expense=total_expense,
        savings=savings,
        budget=budget,

        # Doughnut Chart
        dashboardLabels=labels,
        dashboardValues=values,

        # Monthly Trend Chart
        monthLabels=months,
        monthExpenses=month_expenses,

        # Spending Analysis
        highest_category=highest_category,
        highest_amount=highest_amount,

        food_percent=food_percent,
        travel_percent=travel_percent,
        shopping_percent=shopping_percent,

        # Smart Recommendations
        recommendations=recommendations,

        # Financial Health
        health_score=health_score,
        health_status=health_status,

        # Alerts
        alerts=alerts,
        alerts_count=alerts_count,
        latest_alerts=latest_alerts,
    )