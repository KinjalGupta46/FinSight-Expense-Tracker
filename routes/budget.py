from flask import Blueprint, render_template, request, redirect, session
print("BUDGET.PY LOADED")
from database import mysql
from datetime import datetime

budget_bp = Blueprint("budget", __name__)


@budget_bp.route("/budget", methods=["GET", "POST"])
def budget():

    if "user_id" not in session:
        return redirect("/login")

    cursor = mysql.connection.cursor()

    month = datetime.now().month
    year = datetime.now().year

    # ================= Save / Update Budget =================

    if request.method == "POST":

        amount = request.form["budget"]

        cursor.execute("""
            SELECT id
            FROM budgets
            WHERE user_id=%s
            AND month=%s
            AND year=%s
        """, (
            session["user_id"],
            month,
            year
        ))

        data = cursor.fetchone()

        if data:

            cursor.execute("""
                UPDATE budgets
                SET monthly_budget=%s
                WHERE id=%s
            """, (
                amount,
                data[0]
            ))

        else:

            cursor.execute("""
                INSERT INTO budgets
                (
                    user_id,
                    monthly_budget,
                    month,
                    year
                )
                VALUES(%s,%s,%s,%s)
            """, (
                session["user_id"],
                amount,
                month,
                year
            ))

        mysql.connection.commit()

        return redirect("/budget")

    # ================= Current Budget =================

    cursor.execute("""
        SELECT monthly_budget
        FROM budgets
        WHERE user_id=%s
        AND month=%s
        AND year=%s
    """, (
        session["user_id"],
        month,
        year
    ))

    data = cursor.fetchone()

    budget = float(data[0]) if data else 0

    # ================= Current Month Expense =================

    cursor.execute("""
        SELECT IFNULL(SUM(amount),0)
        FROM expenses
        WHERE user_id=%s
        AND MONTH(expense_date)=%s
        AND YEAR(expense_date)=%s
    """, (
        session["user_id"],
        month,
        year
    ))

    expense = float(cursor.fetchone()[0])

    # ================= Calculations =================

    remaining = budget - expense

    if budget > 0:
        used = round((expense / budget) * 100, 2)
    else:
        used = 0

    if used < 70:
        status = "Safe ✅"
    elif used < 100:
        status = "Warning ⚠️"
    else:
        status = "Exceeded ❌"

    cursor.close()
    print("Budget =", budget)
    print("Expense =", expense)
    print("Remaining =", remaining)
    print("Used =", used)
    print("Status =", status)
    return render_template(
        "budget.html",
        budget=budget,
        expense=expense,
        remaining=remaining,
        used=used,
        status=status
    )