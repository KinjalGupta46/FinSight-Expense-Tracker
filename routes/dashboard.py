from flask import Blueprint, render_template, session, redirect, url_for
from database import mysql

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():

    # ---------------- Login Check ---------------- #
    if "user_id" not in session:
       return redirect(url_for("login"))

    cursor = mysql.connection.cursor()

    # =====================================================
    # MONTHLY INCOME
    # =====================================================
    cursor.execute("""
        SELECT monthly_income
        FROM users
        WHERE id=%s
    """, (session["user_id"],))

    result = cursor.fetchone()
    income = float(result[0]) if result and result[0] else 0

    # =====================================================
    # TOTAL EXPENSE
    # =====================================================
    cursor.execute("""
        SELECT IFNULL(SUM(amount),0)
        FROM expenses
        WHERE user_id=%s
    """, (session["user_id"],))

    expense = float(cursor.fetchone()[0])
    savings = income - expense

    # =====================================================
    # BUDGET
    # =====================================================
    cursor.execute("""
        SELECT monthly_budget
        FROM budgets
        WHERE user_id=%s
        ORDER BY id DESC
        LIMIT 1
    """, (session["user_id"],))

    budget_data = cursor.fetchone()

    if budget_data and float(budget_data[0]) > 0:
        budget = round((expense / float(budget_data[0])) * 100, 2)
    else:
        budget = 0

    # =====================================================
    # BUDGET DETAILS
    # =====================================================
    if budget_data and float(budget_data[0]) > 0:
        budget_amount = float(budget_data[0])
        budget_used = expense
        budget_remaining = max(0, budget_amount - budget_used)
        budget = round((budget_used / budget_amount) * 100, 2)
    else:
        budget_amount = 0
        budget_used = expense
        budget_remaining = 0
        budget = 0

    # =====================================================
    # QUICK STATISTICS
    # =====================================================
    cursor.execute("""
        SELECT
            IFNULL(MAX(amount),0),
            IFNULL(AVG(amount),0),
            COUNT(*)
        FROM expenses
        WHERE user_id=%s
    """, (session["user_id"],))

    stats = cursor.fetchone()

    highest_expense = float(stats[0])
    average_expense = round(float(stats[1]), 2)
    total_transactions = stats[2]

    cursor.execute("""
        SELECT
            category,
            COUNT(*)
        FROM expenses
        WHERE user_id=%s
        GROUP BY category
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """, (session["user_id"],))

    category = cursor.fetchone()
    most_used_category = category[0] if category else "N/A"

    # =====================================================
    # RECENT TRANSACTIONS
    # =====================================================
    cursor.execute("""
        SELECT
            expense_date,
            category,
            payment_mode,
            amount
        FROM expenses
        WHERE user_id=%s
        ORDER BY expense_date DESC
        LIMIT 5
    """, (session["user_id"],))

    transactions = cursor.fetchall()

    # =====================================================
    # EXPENSE BREAKDOWN CHART
    # =====================================================
    cursor.execute("""
        SELECT
            category,
            SUM(amount)
        FROM expenses
        WHERE user_id=%s
        GROUP BY category
    """, (session["user_id"],))

    category_data = cursor.fetchall()

    labels = [row[0] for row in category_data]
    values = [float(row[1]) for row in category_data]

    # =====================================================
    # MONTHLY TREND CHART
    # =====================================================
    cursor.execute("""
        SELECT
            MONTH(expense_date),
            SUM(amount)
        FROM expenses
        WHERE user_id=%s
        GROUP BY MONTH(expense_date)
        ORDER BY MONTH(expense_date)
    """, (session["user_id"],))

    monthly_data = cursor.fetchall()

    months = [row[0] for row in monthly_data]
    monthly_values = [float(row[1]) for row in monthly_data]
        # =====================================================
    # INVESTMENT SUMMARY
    # =====================================================
    cursor.execute("""
        SELECT
            IFNULL(SUM(quantity * purchase_price),0),
            IFNULL(SUM(quantity * current_price),0)
        FROM investments
        WHERE user_id=%s
    """, (session["user_id"],))

    investment_summary = cursor.fetchone()

    total_investment = float(investment_summary[0])
    current_portfolio = float(investment_summary[1])

    portfolio_profit = current_portfolio - total_investment

    if total_investment > 0:
        portfolio_return = round(
            (portfolio_profit / total_investment) * 100,
            2
        )
    else:
        portfolio_return = 0

    # =====================================================
    # TOP HOLDINGS
    # =====================================================
    cursor.execute("""
        SELECT
            investment_name,
            investment_type,
            quantity * current_price AS current_value,
            quantity * purchase_price AS invested_value,
            ROUND(
                (
                    (quantity * current_price) -
                    (quantity * purchase_price)
                ) / NULLIF(quantity * purchase_price,0) * 100,
                2
            ) AS returns_percent
        FROM investments
        WHERE user_id=%s
        ORDER BY current_value DESC
        LIMIT 5
    """, (session["user_id"],))

    top_holdings = cursor.fetchall()

    # =====================================================
    # ASSET ALLOCATION CHART
    # =====================================================
    cursor.execute("""
        SELECT
            investment_type,
            SUM(quantity * current_price)
        FROM investments
        WHERE user_id=%s
        GROUP BY investment_type
    """, (session["user_id"],))

    allocation = cursor.fetchall()

    allocation_labels = [row[0] for row in allocation]
    allocation_values = [float(row[1]) for row in allocation]

    # =====================================================
    # PORTFOLIO PERFORMANCE
    # =====================================================
    cursor.execute("""
        SELECT
            MONTH(purchase_date),
            SUM(quantity * current_price)
        FROM investments
        WHERE user_id=%s
        GROUP BY MONTH(purchase_date)
        ORDER BY MONTH(purchase_date)
    """, (session["user_id"],))

    portfolio_data = cursor.fetchall()

    portfolio_months = [row[0] for row in portfolio_data]
    portfolio_values = [float(row[1]) for row in portfolio_data]

    # =====================================================
    # GOAL SUMMARY
    # =====================================================
    cursor.execute("""
        SELECT
            COUNT(*),
            IFNULL(SUM(target_amount),0),
            IFNULL(SUM(saved_amount),0)
        FROM financial_goals
        WHERE user_id=%s
    """, (session["user_id"],))

    goal_summary = cursor.fetchone()

    total_goals = goal_summary[0]
    total_target = float(goal_summary[1])
    total_saved = float(goal_summary[2])

    if total_target > 0:
        goal_progress = round(
            (total_saved / total_target) * 100,
            2
        )
    else:
        goal_progress = 0


    

    # =====================================================
    # RECENT GOALS
    # =====================================================
    cursor.execute("""
        SELECT
            goal_name,
            target_amount,
            saved_amount,
            ROUND(
                (saved_amount / NULLIF(target_amount,0)) * 100,
                2
            )
        FROM financial_goals
        WHERE user_id=%s
        ORDER BY id DESC
        LIMIT 5
    """, (session["user_id"],))

    goal_progress_list = cursor.fetchall()

        # =====================================================
    # FINANCIAL HEALTH SCORE
    # =====================================================
    health_score = 100

    health_score -= min(budget, 40)

    if savings <= 0:
        health_score -= 20

    if goal_progress < 50:
        health_score -= 15

    if portfolio_return < 0:
        health_score -= 10

    health_score = max(0, round(health_score))

    if health_score >= 80:
        health_status = "Excellent"
    elif health_score >= 60:
        health_status = "Good"
    elif health_score >= 40:
        health_status = "Average"
    else:
        health_status = "Poor"

     # =====================================================
    # LAST 6 MONTHS EXPENSE TREND
    # =====================================================

    cursor.execute("""
    SELECT
        DATE_FORMAT(expense_date,'%%b %%Y') AS month_name,
        SUM(amount)
    FROM expenses
    WHERE user_id=%s
      AND expense_date >= DATE_SUB(CURDATE(), INTERVAL 5 MONTH)
    GROUP BY
        YEAR(expense_date),
        MONTH(expense_date),
        DATE_FORMAT(expense_date,'%%b %%Y')
    ORDER BY
        YEAR(expense_date),
        MONTH(expense_date)
""", (session["user_id"],))
    last6 = cursor.fetchall()

    last6_labels = [row[0] for row in last6]
    last6_values = [float(row[1]) for row in last6]

    # =====================================================
    # INCOME VS EXPENSE
    # =====================================================

    income_vs_expense = [income, expense]
    
    cursor.close()

    return render_template(
        "dashboard.html",

        # User
        name=session["name"],

        # Finance Summary
        income=income,
        expense=expense,
        savings=savings,
        budget=budget,

        # Budget Details
        budget_amount=budget_amount,
        budget_used=budget_used,
        budget_remaining=budget_remaining,

        # Quick Statistics
        highest_expense=highest_expense,
        average_expense=average_expense,
        total_transactions=total_transactions,
        most_used_category=most_used_category,

        # Expense Charts
        labels=labels,
        values=values,

        # Monthly Trend
        months=months,
        monthly_values=monthly_values,

        # Recent Transactions
        transactions=transactions,

        # Investment Summary
        total_investment=total_investment,
        current_portfolio=current_portfolio,
        portfolio_profit=portfolio_profit,
        portfolio_return=portfolio_return,

        # Top Holdings
        top_holdings=top_holdings,

        # Asset Allocation
        allocation_labels=allocation_labels,
        allocation_values=allocation_values,

        # Portfolio Performance
        portfolio_months=portfolio_months,
        portfolio_values=portfolio_values,

        # Goal Summary
        total_goals=total_goals,
        total_target=total_target,
        total_saved=total_saved,
        goal_progress=goal_progress,

        # Recent Goals
        goal_progress_list=goal_progress_list,

        # Financial Health
        health_score=health_score,
        health_status=health_status,

        last6_labels=last6_labels,
        last6_values=last6_values,

        income_vs_expense=income_vs_expense,
    )