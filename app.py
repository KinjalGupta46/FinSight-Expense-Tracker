from flask import Flask, render_template, request, redirect, session, Response
from reportlab.lib import styles
from config import Config
from database import mysql

from routes.investment import investment_bp
from routes.goal import goal_bp
from routes.dashboard import dashboard_bp
from routes.analytics import analytics_bp
from routes.insights import insights_bp
from routes.alerts import alerts_bp
from routes.notifications import notifications_bp

from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    PageBreak
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.colors import PCMYKColor
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.textlabels import Label


import bcrypt
import re
import csv
import io
from datetime import datetime


app = Flask(__name__)
from datetime import timedelta

app.permanent_session_lifetime = timedelta(minutes=30)

app.config.from_object(Config)

mysql.init_app(app)

# ---------------- BLUEPRINTS ---------------- #

app.register_blueprint(goal_bp)
app.register_blueprint(investment_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(insights_bp)
app.register_blueprint(alerts_bp)
app.register_blueprint(notifications_bp)

# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return redirect("/login")



# ---------------- REGISTER ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip().lower()
        phone = request.form["phone"].strip()

        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        monthly_income = request.form["monthly_income"]
        income_source = request.form["income_source"]
        financial_preference = request.form["financial_preference"]


        # Password Validation

        password_pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)"
            r"(?=.*[@$!%*?&.#])"
            r"[A-Za-z\d@$!%*?&.#]{8,}$"
        )


        if not re.match(password_pattern, password):

            return """
            <script>
            alert("Password must contain at least 8 characters, one uppercase, one lowercase, one number and one special character.");
            window.history.back();
            </script>
            """


        if password != confirm_password:

            return """
            <script>
            alert("Passwords do not match.");
            window.history.back();
            </script>
            """



        # Phone Validation

        if not phone.isdigit() or len(phone) != 10:

            return """
            <script>
            alert("Phone number must contain exactly 10 digits.");
            window.history.back();
            </script>
            """



        cursor = mysql.connection.cursor()



        # Duplicate Email Check

        cursor.execute(
            "SELECT id FROM users WHERE email=%s",
            (email,)
        )


        if cursor.fetchone():

            cursor.close()

            return """
            <script>
            alert("Email already registered!");
            window.history.back();
            </script>
            """



        # Duplicate Phone Check

        cursor.execute(
            "SELECT id FROM users WHERE phone=%s",
            (phone,)
        )


        if cursor.fetchone():

            cursor.close()

            return """
            <script>
            alert("Phone number already registered!");
            window.history.back();
            </script>
            """



        # Password Hashing

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")



        # Insert User

        cursor.execute("""
            INSERT INTO users
            (
                full_name,
                email,
                phone,
                password,
                monthly_income,
                income_source,
                financial_preference
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            full_name,
            email,
            phone,
            hashed_password,
            monthly_income,
            income_source,
            financial_preference
        ))


        mysql.connection.commit()

        cursor.close()


        return redirect("/login")



    return render_template("register.html")

# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":


        email = request.form["email"]
        password = request.form["password"]


        cursor = mysql.connection.cursor()


        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )


        user = cursor.fetchone()


        cursor.close()



        if user and bcrypt.checkpw(
            password.encode("utf-8"),
            user[4].encode("utf-8")
        ):


            session["user_id"] = user[0]
            session.permanent = True
            session["name"] = user[1]
            session["role"] = user[9]



            if user[9] == "admin":

                return redirect("/admin")

            else:

                return redirect("/dashboard")



        return "Invalid Email or Password"



    return render_template("login.html")





# ---------------- PROFILE ---------------- #

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")



    cursor = mysql.connection.cursor()



    cursor.execute("""
        SELECT
            full_name,
            email,
            phone,
            monthly_income,
            income_source,
            financial_preference,
            currency,
            role
        FROM users
        WHERE id=%s
    """,
    (session["user_id"],))



    user = cursor.fetchone()



    cursor.close()



    return render_template(
        "profile.html",
        user=user
    )





# ---------------- FORGOT PASSWORD ---------------- #

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return """
            <script>
            alert("Passwords do not match.");
            window.history.back();
            </script>
            """

        password_pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)"
            r"(?=.*[@$!%*?&.#])"
            r"[A-Za-z\d@$!%*?&.#]{8,}$"
        )

        if not re.match(password_pattern, password):
            return """
            <script>
            alert("Password is not strong enough.");
            window.history.back();
            </script>
            """

        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        if not user:
            cursor.close()
            return """
            <script>
            alert("Email not found.");
            window.history.back();
            </script>
            """

        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        cursor.execute(
            "UPDATE users SET password=%s WHERE email=%s",
            (hashed, email)
        )

        mysql.connection.commit()
        cursor.close()

        return """
        <script>
        alert("Password Updated Successfully.");
        window.location='/login';
        </script>
        """

    return render_template("forgot_password.html")


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ---------------- EXPENSES ---------------- #

@app.route("/expenses", methods=["GET", "POST"])
def expenses():

    if "user_id" not in session:
        return redirect("/login")

    cursor = mysql.connection.cursor()

    if request.method == "POST":

        try:
            amount = float(request.form["amount"])

            if amount <= 0:
                raise ValueError

        except ValueError:
            return """
            <script>
            alert("Please enter a valid amount.");
            history.back();
            </script>
            """

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

    cursor.execute("""
        SELECT
            COUNT(*),
            IFNULL(SUM(amount),0),
            IFNULL(MAX(amount),0)
        FROM expenses
        WHERE user_id=%s
    """, (session["user_id"],))

    stats = cursor.fetchone()

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
        query += " AND description LIKE %s"
        params.append(f"%{search}%")

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
        stats=stats
    )

# ---------------- DELETE EXPENSE ---------------- #

@app.route("/delete-expense/<int:id>")
def delete_expense(id):

    if "user_id" not in session:
        return redirect("/login")



    cursor = mysql.connection.cursor()



    cursor.execute("""
        DELETE FROM expenses
        WHERE id=%s
        AND user_id=%s

    """,
    (
        id,
        session["user_id"]
    ))



    mysql.connection.commit()



    cursor.close()



    return redirect("/expenses")





# ---------------- BUDGET ---------------- #

@app.route("/budget", methods=["GET","POST"])
def budget():

    if "user_id" not in session:
        return redirect("/login")



    cursor = mysql.connection.cursor()



    month = datetime.now().month
    year = datetime.now().year



    # Save Budget

    if request.method == "POST":


        budget = request.form["budget"]



        cursor.execute("""
            SELECT id
            FROM budgets
            WHERE user_id=%s
            AND month=%s
            AND year=%s

        """,
        (
            session["user_id"],
            month,
            year
        ))



        existing = cursor.fetchone()



        if existing:


            cursor.execute("""
                UPDATE budgets
                SET monthly_budget=%s
                WHERE id=%s

            """,
            (
                budget,
                existing[0]
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
                VALUES (%s,%s,%s,%s)

            """,
            (
                session["user_id"],
                budget,
                month,
                year
            ))



        mysql.connection.commit()



        return redirect("/budget")





    # Current Budget

    cursor.execute("""
        SELECT monthly_budget
        FROM budgets
        WHERE user_id=%s
        AND month=%s
        AND year=%s

    """,
    (
        session["user_id"],
        month,
        year
    ))



    budget_data = cursor.fetchone()



    budget = 0



    if budget_data:

        budget = float(
            budget_data[0]
        )





    # Total Expense

    cursor.execute("""
        SELECT IFNULL(SUM(amount),0)
        FROM expenses
        WHERE user_id=%s

    """,
    (
        session["user_id"],
    ))



    expense = float(
        cursor.fetchone()[0]
    )




    remaining = budget - expense



    used = 0



    if budget > 0:

        used = round(
            (expense / budget) * 100,
            2
        )



    if used < 70:

        status = "Safe ✅"


    elif used < 100:

        status = "Warning ⚠️"


    else:

        status = "Exceeded ❌"




    cursor.close()



    return render_template(
        "budget.html",
        budget=budget,
        expense=expense,
        remaining=remaining,
        used=used,
        status=status
    )





# ---------------- REPORTS ---------------- #

@app.route("/reports")
def reports():

    if "user_id" not in session:
        return redirect("/login")

    cursor = mysql.connection.cursor()

    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")

    # ---------- Summary ----------

    summary_query = """
        SELECT
            COUNT(*),
            IFNULL(SUM(amount),0),
            IFNULL(AVG(amount),0),
            IFNULL(MAX(amount),0)
        FROM expenses
        WHERE user_id=%s
    """

    summary_params = [session["user_id"]]

    if from_date:
        summary_query += " AND expense_date >= %s"
        summary_params.append(from_date)

    if to_date:
        summary_query += " AND expense_date <= %s"
        summary_params.append(to_date)

    cursor.execute(summary_query, tuple(summary_params))

    summary = cursor.fetchone()

    total_expenses = summary[0]
    total_amount = float(summary[1])
    average = round(float(summary[2]), 2)
    highest = float(summary[3])

       # Total Categories
    cursor.execute("""
        SELECT COUNT(DISTINCT category)
        FROM expenses
        WHERE user_id=%s
    """, (session["user_id"],))
    total_categories = cursor.fetchone()[0]

    # Current Budget
    cursor.execute("""
        SELECT monthly_budget
        FROM budgets
        WHERE user_id=%s
        ORDER BY id DESC
        LIMIT 1
    """, (session["user_id"],))

    budget_data = cursor.fetchone()
    current_budget = float(budget_data[0]) if budget_data else 0

    budget_left = max(current_budget - total_amount, 0)

    budget_used = 0
    if current_budget > 0:
        budget_used = round((total_amount / current_budget) * 100, 1)

    # Report Table
    report_query = """
        SELECT
            expense_date,
            category,
            payment_mode,
            description,
            amount
        FROM expenses
        WHERE user_id=%s
    """

    report_params = [session["user_id"]]

    if from_date:
        report_query += " AND expense_date >= %s"
        report_params.append(from_date)

    if to_date:
        report_query += " AND expense_date <= %s"
        report_params.append(to_date)

    report_query += " ORDER BY expense_date DESC"

    cursor.execute(report_query, tuple(report_params))
    reports = cursor.fetchall()

    cursor.execute("""
        SELECT
            DATE_FORMAT(MIN(expense_date), '%%b') AS month_name,
            SUM(amount)
        FROM expenses
        WHERE user_id=%s
        GROUP BY YEAR(expense_date), MONTH(expense_date)
        ORDER BY YEAR(expense_date), MONTH(expense_date)
    """, (session["user_id"],))

    chart = cursor.fetchall()

    chart_labels = [row[0] for row in chart]
    chart_values = [float(row[1]) for row in chart]

    cursor.execute("""
        SELECT
            category,
            SUM(amount)
        FROM expenses
        WHERE user_id=%s
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """, (session["user_id"],))

    category_chart = cursor.fetchall()

    category_labels = [row[0] for row in category_chart]
    category_values = [float(row[1]) for row in category_chart]

    cursor.close()

    return render_template(
        "reports.html",
        total_expenses=total_expenses,
        total_amount=total_amount,
        average=average,
        highest=highest,
        reports=reports,
        chart_labels=chart_labels,
        chart_values=chart_values,
        category_labels=category_labels,
        category_values=category_values,
        total_categories=total_categories,
        current_budget=current_budget,
        budget_left=budget_left,
        budget_used=budget_used
    )
# ---------------- EXPORT EXPENSES CSV ---------------- #

@app.route("/export-expenses")
def export_expenses():

    if "user_id" not in session:
        return redirect("/login")

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            expense_date,
            category,
            payment_mode,
            description,
            amount
        FROM expenses
        WHERE user_id=%s
        ORDER BY expense_date DESC
    """, (session["user_id"],))

    expenses = cursor.fetchall()

    cursor.close()

    output = io.StringIO()
    writer = csv.writer(output)

    # CSV Header
    writer.writerow([
        "Date",
        "Category",
        "Payment Mode",
        "Description",
        "Amount"
    ])

    # CSV Data
    for expense in expenses:
        writer.writerow(expense)

    output.seek(0)

    return Response(
    output.getvalue(),
    mimetype="application/octet-stream",
    headers={
        "Content-Disposition":
        "attachment; filename=expense_report.csv"
    }
)

@app.route("/export-pdf")
def export_pdf():

    if "user_id" not in session:
        return redirect("/login")

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT expense_date, category, amount, description
        FROM expenses
        WHERE user_id=%s
        ORDER BY expense_date DESC
    """, (session["user_id"],))

    expenses = cursor.fetchall()

    # =====================================================
# USER FINANCIAL SUMMARY
# =====================================================

    # Monthly Income
    cursor.execute("""
        SELECT monthly_income
        FROM users
        WHERE id=%s
    """, (session["user_id"],))

    income_data = cursor.fetchone()
    monthly_income = float(income_data[0]) if income_data and income_data[0] else 0

    # Current Budget
    cursor.execute("""
        SELECT monthly_budget
        FROM budgets
        WHERE user_id=%s
        ORDER BY id DESC
        LIMIT 1
    """, (session["user_id"],))

    budget_data = cursor.fetchone()
    budget_amount = float(budget_data[0]) if budget_data else 0

    # Budget Used %
    budget_used = 0

    if budget_amount > 0:
        budget_used = round(
            (sum(float(x[2]) for x in expenses) / budget_amount) * 100,
            2
        )

    # Savings
    total_expense = sum(float(x[2]) for x in expenses)
    savings = monthly_income - total_expense

    # User Name
    cursor.execute(
        "SELECT full_name FROM users WHERE id=%s",
        (session["user_id"],)
    )

    user_name = cursor.fetchone()[0]

    cursor.close()

    # ================= PDF Generation ================= #

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    cover_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=24,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=13,
        textColor=colors.grey,
        spaceAfter=10
    )

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        fontSize=18,
        textColor=colors.HexColor("#2563EB"),
        spaceAfter=25
    )

    elements.append(
        Paragraph(
            "FinSight",
            cover_style
        )
    )

    elements.append(
        Paragraph(
            "Personal Finance & Investment Intelligence Platform",
            subtitle_style
        )
    )

    elements.append(
        Paragraph(
            "FINANCIAL ANALYSIS REPORT",
            title_style
        )
    )
   
    report_id = f"FS-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    info = [
        ["Prepared For", user_name],
        ["Report ID", report_id],
        ["Generated On", datetime.now().strftime("%d %B %Y")],
        ["Generated Time", datetime.now().strftime("%I:%M %p")]
    ]

    info_table = Table(
        info,
        colWidths=[150, 250]
    )

    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#1E3A8A")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),

        ("BACKGROUND", (1, 0), (1, -1), colors.whitesmoke),

        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8)
    ]))

    elements.append(info_table)
    elements.append(
        Paragraph(
            "<br/><br/>",
            styles["Normal"]
        )
    )

        # ================= Executive Summary ================= #

    elements.append(
        Paragraph(
            "<b><font size='16' color='#1E3A8A'>Executive Summary</font></b>",
            styles["Heading2"]
        )
    )

    total_amount = sum(float(row[2]) for row in expenses)

    average = total_amount / len(expenses) if expenses else 0

    highest = max(float(row[2]) for row in expenses) if expenses else 0

    financial_health = "Excellent"

    financial_health = "🟢 Excellent"

    if budget_used <= 50:
        financial_health = "🟢 Excellent"

    elif budget_used <= 75:
        financial_health = "🟡 Good"

    elif budget_used <= 100:
        financial_health = "🟠 Warning"

    else:
        financial_health = "🔴 Critical"
    summary_data = [
        ["Monthly Income", f"Rs. {monthly_income:,.2f}"],
        ["Total Expenses", f"Rs. {total_amount:,.2f}"],
        ["Savings", f"Rs. {savings:,.2f}"],
        ["Budget Used", f"{budget_used}%"],
        ["Average Expense", f"Rs. {average:,.2f}"],
        ["Highest Expense", f"Rs. {highest:,.2f}"],
        ["Financial Health", financial_health]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[180, 220]
    )

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#2563EB")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),

        ("BACKGROUND", (1, 0), (1, -1), colors.whitesmoke),

        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8)
    ]))

    elements.append(summary_table)

    elements.append(summary_table)

    elements.append(PageBreak())

    # ================= Expense Details ================= #

    elements.append(
        Paragraph(
            "<b><font size='16' color='#1E3A8A'>Expense Details</font></b>",
            styles["Heading2"]
        )
    )

    data = [
        ["Date", "Category", "Amount (Rs.)", "Description"]
    ]

    for row in expenses:
        data.append([
            str(row[0]),
            row[1],
            f"Rs. {float(row[2]):,.2f}",
            row[3] if row[3] else "-"
        ])

    table = Table(
        data,
        colWidths=[80, 120, 100, 220],
        repeatRows=1
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),

        ("FONTSIZE", (0, 0), (-1, -1), 10),

        ("ALIGN", (2, 1), (2, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

        ("ROWBACKGROUNDS",
         (0, 1),
         (-1, -1),
         [colors.whitesmoke, colors.beige])
    ]))

    elements.append(table)

    elements.append(PageBreak())

        # ================= Expense Category Chart ================= #

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE user_id=%s
        GROUP BY category
    """, (session["user_id"],))

    chart_data = cursor.fetchall()

    cursor.close()

    if chart_data:

        elements.append(
            Paragraph(
                "<b><font size='16' color='#1E3A8A'>Expense Distribution</font></b>",
                styles["Heading2"]
            )
        )

        drawing = Drawing(400, 220)

        pie = Pie()

        pie.x = 80
        pie.y = 20
        pie.width = 180
        pie.height = 180

        pie.data = [float(x[1]) for x in chart_data]

        pie.labels = [x[0] for x in chart_data]

        pie.slices.strokeWidth = 0.5

        pie.slices[0].fillColor = colors.HexColor("#2563EB")

        if len(chart_data) > 1:
            pie.slices[1].fillColor = colors.HexColor("#10B981")

        if len(chart_data) > 2:
            pie.slices[2].fillColor = colors.HexColor("#F59E0B")

        if len(chart_data) > 3:
            pie.slices[3].fillColor = colors.HexColor("#EF4444")

        if len(chart_data) > 4:
            pie.slices[4].fillColor = colors.HexColor("#8B5CF6")

        drawing.add(pie)

        elements.append(drawing)

        elements.append(
            Paragraph(
                "<br/>",
                styles["Normal"]
            )
        )
            # ================= Monthly Expense Trend ================= #

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            DATE_FORMAT(MIN(expense_date), '%%b') AS month_name,
            SUM(amount)
        FROM expenses
        WHERE user_id=%s
        GROUP BY YEAR(expense_date), MONTH(expense_date)
        ORDER BY YEAR(expense_date), MONTH(expense_date)
    """, (session["user_id"],))

    monthly_data = cursor.fetchall()

    cursor.close()

    if monthly_data:

        elements.append(
            Paragraph(
                "<b><font size='16' color='#1E3A8A'>Monthly Expense Trend</font></b>",
                styles["Heading2"]
            )
        )

        drawing = Drawing(450, 250)

        chart = VerticalBarChart()

        chart.x = 50
        chart.y = 40
        chart.width = 320
        chart.height = 170

        chart.data = [
            [float(row[1]) for row in monthly_data]
        ]

        chart.categoryAxis.categoryNames = [
            row[0] for row in monthly_data
        ]

        chart.valueAxis.valueMin = 0
        chart.barWidth = 20
        chart.groupSpacing = 15

        chart.bars[0].fillColor = colors.HexColor("#2563EB")

        drawing.add(chart)

        elements.append(drawing)

    elements.append(Paragraph("<br/><br/>", styles["Normal"]))


    elements.append(
        Paragraph(
            "<b>Confidential</b><br/>"
            "This report is intended solely for the account holder and should not be shared without permission.",
            styles["Italic"]
        )
    )

    elements.append(Paragraph("<br/>", styles["Normal"]))

    elements.append(
        Paragraph(
            "<font size='9' color='grey'>"
            "Generated by FinSight | Personal Finance & Investment Intelligence Platform"
            "<br/>© 2026 FinSight. All Rights Reserved."
            "</font>",
            styles["Normal"]
        )
    )

    def add_page_number(canvas, doc):
        canvas.saveState()

        canvas.setFont("Helvetica", 9)

        canvas.setFillColor(colors.grey)

        canvas.drawString(
            40,
            25,
            "Generated by FinSight | Personal Finance & Investment Intelligence Platform"
        )

        page_num = canvas.getPageNumber()

        canvas.drawRightString(
            550,
            25,
            f"Page {page_num}"
        )

        canvas.restoreState()
    
    doc.build(
        elements,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"FinSight_Report_{datetime.now().strftime('%d%m%Y')}.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)