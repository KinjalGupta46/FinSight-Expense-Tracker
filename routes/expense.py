from flask import Blueprint, render_template, request, redirect, session, Response
from database import mysql
import csv

expense_bp = Blueprint("expense", __name__)


# =======================
# View + Add + Search Expenses
# =======================

@expense_bp.route("/expenses", methods=["GET", "POST"])
def expenses():

    if "user_id" not in session:
        return redirect("/login")

    cursor = mysql.connection.cursor()

    # Add Expense
    if request.method == "POST":

        amount = request.form["amount"]
        category = request.form["category"]
        payment_mode = request.form["payment_mode"]
        description = request.form["description"]
        expense_date = request.form["expense_date"]

        cursor.execute("""
            INSERT INTO expenses
            (
                user_id,
                amount,
                category,
                payment_mode,
                description,
                expense_date
            )
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            session["user_id"],
            amount,
            category,
            payment_mode,
            description,
            expense_date
        ))

        mysql.connection.commit()

       # Statistics
    cursor.execute("""
        SELECT
            COUNT(*),
            IFNULL(SUM(amount),0),
            IFNULL(MAX(amount),0)
        FROM expenses
        WHERE user_id=%s
    """, (session["user_id"],))

    stats = cursor.fetchone()

    # Search & Filter
    search = request.args.get("search", "")
    category = request.args.get("category", "")
    date = request.args.get("date", "")
    sort = request.args.get("sort", "new")

    query = """
        SELECT
            id,
            amount,
            category,
            payment_mode,
            description,
            expense_date
        FROM expenses
        WHERE user_id=%s
    """

    params = [session["user_id"]]

    if search:

        query += """
            AND (
                description LIKE %s
                OR category LIKE %s
            )
        """

        params.extend([
            f"%{search}%",
            f"%{search}%"
        ])

    if category:

        query += " AND category=%s"
        params.append(category)

    if date:

        query += " AND expense_date=%s"
        params.append(date)

    if sort == "old":

        query += " ORDER BY expense_date ASC"

    elif sort == "high":

        query += " ORDER BY amount DESC"

    elif sort == "low":

        query += " ORDER BY amount ASC"

    else:

        query += " ORDER BY expense_date DESC"

    cursor.execute(query, tuple(params))

    expenses = cursor.fetchall()

    cursor.close()

    return render_template(
        "expenses.html",
        expenses=expenses,
        stats=stats,
        search=search,
        category=category,
        date=date,
        sort=sort
    )

# =======================
# Edit Expense
# =======================

@expense_bp.route("/edit-expense/<int:id>", methods=["GET", "POST"])
def edit_expense(id):

    if "user_id" not in session:
        return redirect("/login")

    cursor = mysql.connection.cursor()

    if request.method == "POST":

        amount = request.form["amount"]
        category = request.form["category"]
        payment_mode = request.form["payment_mode"]
        description = request.form["description"]
        expense_date = request.form["expense_date"]

        cursor.execute("""
            UPDATE expenses
            SET
                amount=%s,
                category=%s,
                payment_mode=%s,
                description=%s,
                expense_date=%s
            WHERE id=%s
            AND user_id=%s
        """, (
            amount,
            category,
            payment_mode,
            description,
            expense_date,
            id,
            session["user_id"]
        ))

        mysql.connection.commit()

        cursor.close()

        return redirect("/expenses")

    cursor.execute("""
        SELECT
            id,
            amount,
            category,
            payment_mode,
            description,
            expense_date
        FROM expenses
        WHERE id=%s
        AND user_id=%s
    """, (
        id,
        session["user_id"]
    ))

    expense = cursor.fetchone()

    cursor.close()

    return render_template(
        "edit_expense.html",
        expense=expense
    )


# =======================
# Delete Expense
# =======================

@expense_bp.route("/delete-expense/<int:id>")
def delete_expense(id):

    if "user_id" not in session:
        return redirect("/login")

    cursor = mysql.connection.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id=%s
        AND user_id=%s
    """, (
        id,
        session["user_id"]
    ))

    mysql.connection.commit()

    cursor.close()

    return redirect("/expenses")


# =======================
# Export CSV
# =======================

@expense_bp.route("/export-expenses")
def export_expenses():

    if "user_id" not in session:
        return redirect("/login")

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            amount,
            category,
            payment_mode,
            description,
            expense_date
        FROM expenses
        WHERE user_id=%s
    """, (
        session["user_id"],
    ))

    data = cursor.fetchall()

    cursor.close()

    def generate():

        yield "Amount,Category,Payment Mode,Description,Expense Date\n"

        for row in data:
            yield ",".join(map(str, row)) + "\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=expenses.csv"
        }
    )