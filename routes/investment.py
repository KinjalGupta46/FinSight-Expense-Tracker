from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import mysql

investment_bp = Blueprint("investment", __name__)


# -------------------- Add Investment -------------------- #
@investment_bp.route("/add-investment", methods=["GET", "POST"])
def add_investment():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        investment_name = request.form["investment_name"]
        investment_type = request.form["investment_type"]
        quantity = float(request.form["quantity"])
        purchase_price = float(request.form["purchase_price"])
        current_price = float(request.form["current_price"])
        purchase_date = request.form["purchase_date"]

        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO investments
            (
                user_id,
                investment_name,
                investment_type,
                quantity,
                purchase_price,
                current_price,
                purchase_date
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            session["user_id"],
            investment_name,
            investment_type,
            quantity,
            purchase_price,
            current_price,
            purchase_date
        ))

        mysql.connection.commit()
        cursor.close()

        flash("Investment Added Successfully!", "success")
        return redirect(url_for("investment.view_investments"))

    return render_template("add_investment.html")


# -------------------- View Investments -------------------- #
@investment_bp.route("/investments")
def view_investments():

    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor = mysql.connection.cursor()

    # Fetch all investments
    cursor.execute("""
        SELECT
            id,
            investment_name,
            investment_type,
            quantity,
            purchase_price,
            current_price,
            purchase_date,

            (quantity * purchase_price) AS invested_amount,

            (quantity * current_price) AS current_value,

            ((quantity * current_price) - (quantity * purchase_price)) AS profit_loss,

            CASE
                WHEN (quantity * purchase_price) = 0 THEN 0
                ELSE (
                    ((quantity * current_price) - (quantity * purchase_price))
                    / (quantity * purchase_price)
                ) * 100
            END AS return_percentage

        FROM investments
        WHERE user_id=%s
        ORDER BY id DESC
    """, (session["user_id"],))

    investments = cursor.fetchall()

    # Portfolio Summary
    cursor.execute("""
        SELECT
            IFNULL(SUM(quantity * purchase_price), 0),
            IFNULL(SUM(quantity * current_price), 0)
        FROM investments
        WHERE user_id=%s
    """, (session["user_id"],))

    summary = cursor.fetchone()

    total_investment = float(summary[0])
    current_value = float(summary[1])
    profit_loss = current_value - total_investment

    if total_investment > 0:
        overall_return = round((profit_loss / total_investment) * 100, 2)
    else:
        overall_return = 0

    # Asset Allocation
    cursor.execute("""
        SELECT
            investment_type,
            SUM(quantity * current_price)
        FROM investments
        WHERE user_id=%s
        GROUP BY investment_type
    """, (session["user_id"],))

    allocation_data = cursor.fetchall()

    chart_labels = [row[0] for row in allocation_data]
    chart_values = [float(row[1]) for row in allocation_data]

    cursor.close()

    return render_template(
        "investments.html",
        investments=investments,
        total_investment=total_investment,
        current_value=current_value,
        profit_loss=profit_loss,
        overall_return=overall_return,
        chart_labels=chart_labels,
        chart_values=chart_values
    )

# -------------------- Delete Investment -------------------- #
@investment_bp.route("/delete-investment/<int:id>")
def delete_investment(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor = mysql.connection.cursor()

    cursor.execute("""
        DELETE FROM investments
        WHERE id=%s AND user_id=%s
    """, (
        id,
        session["user_id"]
    ))

    mysql.connection.commit()
    cursor.close()

    flash("Investment Deleted Successfully!", "success")

    return redirect(url_for("investment.view_investments"))


# -------------------- Edit Investment -------------------- #
@investment_bp.route("/edit-investment/<int:id>", methods=["GET", "POST"])
def edit_investment(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor = mysql.connection.cursor()

    if request.method == "POST":

        investment_name = request.form["investment_name"]
        investment_type = request.form["investment_type"]
        quantity = float(request.form["quantity"])
        purchase_price = float(request.form["purchase_price"])
        current_price = float(request.form["current_price"])
        purchase_date = request.form["purchase_date"]

        cursor.execute("""
            UPDATE investments
            SET
                investment_name=%s,
                investment_type=%s,
                quantity=%s,
                purchase_price=%s,
                current_price=%s,
                purchase_date=%s
            WHERE id=%s
            AND user_id=%s
        """, (
            investment_name,
            investment_type,
            quantity,
            purchase_price,
            current_price,
            purchase_date,
            id,
            session["user_id"]
        ))

        mysql.connection.commit()
        cursor.close()

        flash("Investment Updated Successfully!", "success")

        return redirect(url_for("investment.view_investments"))

    cursor.execute("""
        SELECT
            investment_name,
            investment_type,
            quantity,
            purchase_price,
            current_price,
            purchase_date
        FROM investments
        WHERE id=%s
        AND user_id=%s
    """, (
        id,
        session["user_id"]
    ))

    investment = cursor.fetchone()

    cursor.close()

    return render_template(
        "edit_investment.html",
        investment=investment
    )