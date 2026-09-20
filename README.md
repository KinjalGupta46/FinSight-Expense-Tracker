# 💰 FinSight — Personal Finance & Investment Intelligence Platform

FinSight is a full-stack personal finance management platform built using **Python, Flask, and MySQL**.

The platform helps users manage their complete financial activity from one place — including income, expenses, budgets, investments, financial goals, analytics, notifications, and downloadable financial reports.

Instead of maintaining multiple spreadsheets or applications, FinSight provides a centralized dashboard where users can monitor their financial health and make better data-driven decisions.

---

## 🌐 Live Demo

🚀 **Live Application:**  
https://finsight-expense-tracker.onrender.com

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Key Features](#-key-features)
- [Core Modules](#-core-modules)
- [Technology Stack](#-technology-stack)
- [Project Architecture](#-project-architecture)
- [Project Structure](#-project-structure)
- [Database Design](#-database-design)
- [Analytics & Intelligence](#-analytics--intelligence)
- [Financial Health Score](#-financial-health-score)
- [Dashboard](#-dashboard)
- [Notifications & Alerts](#-notifications--alerts)
- [Reports](#-reports)
- [Installation](#-installation)
- [Environment Variables](#-environment-variables)
- [Configuration](#-configuration)
- [Running the Project Locally](#-running-the-project-locally)
- [Deployment](#-deployment)
- [Application Workflow](#-application-workflow)
- [Testing](#-testing)
- [Project Highlights](#-project-highlights)
- [Current Scope](#-current-scope)
- [Future Scope](#-future-scope)
- [Screenshots](#-screenshots)
- [Development Tools](#-development-tools)
- [Author](#-author)
- [Acknowledgement](#-acknowledgement)
- [License](#-license)

---

# 📖 Overview

Managing personal finances can become difficult when income, expenses, investments, budgets, and financial goals are tracked using different applications or spreadsheets.

**FinSight** solves this problem by providing a centralized personal finance platform.

Users can:

- Create and manage their account
- Track income and expenses
- Categorize transactions
- Set and monitor budgets
- Track investments
- Create financial goals
- Analyze spending patterns
- Monitor financial health
- View financial dashboards
- Receive financial alerts
- Generate PDF reports
- Generate Excel reports

The application combines financial tracking with analytics to provide users with meaningful insights into their financial activity.

---

# 🎯 Problem Statement

Personal financial information is often fragmented across:

- Bank statements
- Spreadsheets
- Investment applications
- Expense tracking applications
- Notes and manual records

This makes it difficult to get a complete picture of financial health.

FinSight provides a single platform to centralize this information and transform raw financial data into understandable insights.

---

# 💡 Solution

FinSight provides an integrated financial management system where users can manage their:

**Income → Expenses → Budgets → Investments → Goals → Analytics → Reports**

All major financial activities are connected to the user's account, allowing the platform to generate personalized dashboards and financial insights.

---

# ✨ Key Features

## 🔐 1. User Authentication

FinSight provides an authentication system with:

- User registration
- User login
- Logout
- Password hashing
- Session management
- Profile management
- User-specific financial data
- Password validation
- Protected routes

---

## 💸 2. Expense Management

Users can record and manage their daily expenses.

Each expense can contain:

- Date
- Category
- Amount
- Description

Supported categories can include:

- Food
- Shopping
- Travel
- Healthcare
- Education
- Other expenses

Users can view their expense history and analyze where their money is being spent.

---

## 💰 3. Income Management

Users can maintain their income information and use it together with their expenses to understand their savings and overall financial position.

The system can use income information for:

- Savings calculation
- Financial health analysis
- Income vs expense comparison
- Budget planning
- Financial reports

---

## 📊 4. Budget Management

Users can create budgets and monitor their spending against those limits.

The system helps identify:

- Budget utilization
- Overspending
- Remaining budget
- Spending trends
- Budget thresholds

Budget-related alerts can also be generated when spending approaches defined limits.

---

## 📈 5. Investment Tracking

FinSight provides investment portfolio management and tracking.

Users can manage different investment categories such as:

- Stocks
- Mutual Funds
- ETFs
- Bonds
- Gold
- Cash

The platform can display:

- Investment value
- Portfolio allocation
- Gains/Losses
- ROI
- Investment performance

---

## 🎯 6. Financial Goal Planning

Users can create financial goals and track their progress.

Examples:

- Education
- Emergency Fund
- Travel
- Home
- Retirement
- Other savings goals

Users can define:

- Goal name
- Target amount
- Current progress
- Target timeline

The platform provides progress tracking and savings recommendations.

---

# 🧩 Core Modules

FinSight is divided into multiple functional modules.

### Authentication Module

Handles:

- Registration
- Login
- Logout
- Password management
- User sessions

### Dashboard Module

Provides a centralized overview of:

- Income
- Expenses
- Savings
- Budgets
- Investments
- Goals
- Financial health

### Analytics Module

Processes financial data and generates:

- Spending patterns
- Expense distribution
- Monthly trends
- Income vs expense analysis
- Financial health metrics

### Reports Module

Allows users to generate:

- PDF financial reports
- Excel financial reports

### Database Module

Handles:

- User records
- Financial transactions
- Budgets
- Investments
- Goals
- Notifications
- Preferences

---

# 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Database | MySQL |
| Database Connectivity | Flask-MySQLdb |
| Analytics | Pandas, NumPy |
| Authentication | Flask-Login, Werkzeug Security |
| Visualization | Chart.js |
| PDF Reports | ReportLab |
| Excel Reports | OpenPyXL |
| Version Control | Git, GitHub |
| Deployment | Render |
| Cloud Database | Aiven MySQL |
| Development Environment | VS Code |

---

# 🏗️ Project Architecture

FinSight follows a modular Flask architecture.

```text
                    ┌──────────────────────┐
                    │      User / Browser  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   HTML / CSS / JS    │
                    │      Frontend        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Flask App       │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
       Authentication      Finance Logic     Analytics
             │                 │                 │
             │                 │                 ▼
             │                 │          Pandas / NumPy
             │                 │
             └─────────────────┼─────────────────┐
                               │                 │
                               ▼                 ▼
                         MySQL Database       Reports
                                              │
                                     ┌────────┴────────┐
                                     ▼                 ▼
                                   PDF               Excel
```

---

# 📂 Project Structure

The project follows a modular Flask-based structure.

```text
FinSight-Expense-Tracker/
│
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── dashboard.py
│   ├── analytics.py
│   ├── reports.py
│   └── ...
│
├── static/
│   │
│   ├── css/
│   │   ├── analytics.css
│   │   ├── dashboard.css
│   │   ├── forgot.css
│   │   ├── login.css
│   │   ├── Register.css
│   │   └── reports.css
│   │
│   ├── js/
│   │   ├── analytics.js
│   │   ├── dashboard.js
│   │   └── reports.js
│   │
│   └── images/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── analytics.html
│   ├── reports.html
│   └── ...
│
├── config.py
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── venv/
```

### Folder Description

| Folder/File | Purpose |
|---|---|
| `routes/` | Flask application routes and business logic |
| `static/css/` | Application stylesheets |
| `static/js/` | Frontend JavaScript |
| `static/images/` | Images and visual assets |
| `templates/` | HTML templates |
| `config.py` | Application configuration |
| `app.py` | Flask application entry point |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Files excluded from Git |
| `README.md` | Project documentation |
| `venv/` | Local Python virtual environment |

---

# 🗄️ Database Design

FinSight uses a relational **MySQL database**.

The database is designed to maintain separate financial records while connecting them to the corresponding user.

## Core Entities

```text
Users
 │
 ├── Accounts
 │
 ├── Transactions
 │
 ├── Budgets
 │
 ├── Investments
 │
 ├── Goals
 │      │
 │      └── Goal Transactions
 │
 ├── Portfolio History
 │
 ├── Notifications
 │
 └── User Preferences
```

## Main Tables

| Table | Purpose |
|---|---|
| Users | User authentication and profile information |
| Accounts | Financial accounts |
| Transactions | Income and expense records |
| Categories | Expense categories |
| Budgets | Budget limits |
| Investments | Investment holdings |
| Goals | Financial savings goals |
| Goal_Transactions | Goal contributions |
| Portfolio_History | Investment history |
| Notifications | Alerts and notifications |
| User_Preferences | User financial preferences |

All financial records are associated with the relevant user to maintain user-level data separation.

---

# 🧠 Analytics & Intelligence

One of the main components of FinSight is its analytics engine.

Financial data is processed using:

- **Pandas**
- **NumPy**

The analytics module analyzes user financial activity and generates useful information.

## Analytics Include

- Expense distribution
- Monthly expense trends
- Income vs expense comparison
- Spending patterns
- Budget utilization
- Investment performance
- Savings analysis
- Financial health score

### Example

If a user spends significantly more money on a particular category, FinSight can identify that spending pattern and display it through the analytics dashboard.

---

# 🏥 Financial Health Score

FinSight calculates a financial health score using financial indicators such as:

- Income
- Expenses
- Savings
- Budget utilization
- Investment activity
- Goal progress

The score provides users with an easy-to-understand overview of their financial condition.

---

# 📊 Dashboard

The dashboard provides a centralized view of the user's financial information.

It can display:

- Total income
- Total expenses
- Savings
- Budget utilization
- Investment value
- Financial goals
- Expense distribution
- Monthly trends
- Financial health score

Charts and visualizations make financial information easier to understand.

---

# 🔔 Notifications & Alerts

FinSight includes financial notifications and alerts for events such as:

- Budget threshold warnings
- Overspending
- Investment performance
- Goal reminders
- Monthly financial summaries

These alerts help users stay aware of important financial changes.

---

# 📄 Reports

FinSight supports downloadable financial reports.

## 📑 PDF Reports

PDF reports are generated using:

**ReportLab**

Reports can contain:

- Financial summary
- Income
- Expenses
- Savings
- Expense details
- Expense distribution
- Monthly expense trends
- Financial health information

---

## 📊 Excel Reports

Excel reports are generated using:

**OpenPyXL**

Users can export financial information into Excel format for further analysis.

---

# 🔐 Environment Variables

For local development, create a `.env` file or configure the environment variables according to your Flask configuration.

Example:

```env
SECRET_KEY=your_secret_key

MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=finsight
MYSQL_PORT=3306
```

For production deployment, these values should be configured inside the hosting platform's environment variable section instead of committing them to GitHub.

> ⚠️ Never commit real passwords, API keys, database credentials, or secret keys to GitHub.

---

# ⚙️ Configuration

The Flask application reads database configuration from environment variables.

Example `config.py`:

```python
import os


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev_secret_key"
    )

    MYSQL_HOST = os.environ.get(
        "MYSQL_HOST",
        "localhost"
    )

    MYSQL_USER = os.environ.get(
        "MYSQL_USER",
        "root"
    )

    MYSQL_PASSWORD = os.environ.get(
        "MYSQL_PASSWORD",
        ""
    )

    MYSQL_DB = os.environ.get(
        "MYSQL_DB",
        "finsight"
    )

    MYSQL_PORT = int(
        os.environ.get(
            "MYSQL_PORT",
            3306
        )
    )
```

For production, environment variables are provided by the deployment platform.

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/KinjalGupta46/FinSight-Expense-Tracker.git
```

Move into the project directory:

```bash
cd FinSight-Expense-Tracker
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate the environment:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

# 📦 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist, install the required packages manually:

```bash
pip install Flask
pip install flask-mysqldb
pip install mysqlclient
pip install python-dotenv
pip install flask-login
pip install pandas
pip install numpy
pip install reportlab
pip install openpyxl
```

---

# 🗃️ 4. Configure MySQL

Create a MySQL database:

```sql
CREATE DATABASE finsight;
```

Configure the database environment variables:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=finsight
MYSQL_PORT=3306
```

Make sure your MySQL server is running before starting the Flask application.

---

# ▶️ Running the Project Locally

After configuring the database and environment variables:

```bash
python app.py
```

Or, depending on the application entry point:

```bash
flask run
```

The application will normally be available at:

```text
http://127.0.0.1:5000
```

Open the URL in your browser.

---

# 🌐 Deployment

FinSight is deployed as a Flask web application using **Render**.

The production setup consists of:

```text
GitHub Repository
       │
       ▼
     Render
       │
       ▼
  Flask Backend
       │
       ▼
  Aiven MySQL
```

---

# ☁️ Production Database

The deployed version uses a cloud-hosted MySQL database provided through **Aiven**.

The database connection information is provided through environment variables.

Production variables include:

```env
MYSQL_HOST=your_database_host
MYSQL_USER=your_database_user
MYSQL_PASSWORD=your_database_password
MYSQL_DB=your_database_name
MYSQL_PORT=your_database_port
SECRET_KEY=your_secret_key
```

### Important

Never commit real database passwords, secret keys, or other credentials to GitHub.

---

# 🚀 Render Deployment Steps

## Step 1 — Push the Project to GitHub

```bash
git add .
git commit -m "Deploy FinSight application"
git push origin main
```

---

## Step 2 — Create a Web Service on Render

1. Open Render.
2. Create a new **Web Service**.
3. Connect your GitHub repository.
4. Select the `FinSight-Expense-Tracker` repository.

---

## Step 3 — Configure Build Command

Use:

```bash
pip install -r requirements.txt
```

---

## Step 4 — Configure Start Command

For a Flask application using `app.py`:

```bash
gunicorn app:app
```

Make sure the command matches the Flask application entry point used by the project.

---

## Step 5 — Add Environment Variables

Add the production database credentials in Render:

```text
MYSQL_HOST
MYSQL_USER
MYSQL_PASSWORD
MYSQL_DB
MYSQL_PORT
SECRET_KEY
```

These values should match the connection information provided by the cloud MySQL database.

---

## Step 6 — Deploy

After saving the configuration, Render builds and deploys the Flask application.

Every new GitHub push can trigger a new deployment when automatic deployment is enabled.

---

# 🔄 Application Workflow

The general workflow of FinSight is:

```text
                    User
                     │
                     ▼
              Register / Login
                     │
                     ▼
                 Dashboard
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
       Expenses    Budget    Investments
          │          │          │
          │          │          ▼
          │          │       Portfolio
          │          │          │
          └──────────┼──────────┘
                     │
                     ▼
                 Analytics
                     │
                     ▼
             Financial Health
                     │
                     ▼
                  Reports
                 /       \
                ▼         ▼
              PDF       Excel
```

---

# 📊 Example Analytics

FinSight can generate visual analytics such as:

## Expense Distribution

```text
Food
Shopping
Travel
Healthcare
Education
Other
```

This allows users to understand which categories consume most of their spending.

---

## Monthly Expense Trend

The dashboard can visualize monthly spending over time and help users identify increasing or decreasing expense patterns.

---

## Income vs Expense

The platform compares income and expenses to calculate savings and provide a better understanding of financial performance.

---

# 📄 Example Financial Report

A generated financial report may include:

```text
Financial Summary
────────────────────────────

Monthly Income       ₹50,000
Total Expenses        ₹6,200
Savings              ₹43,800
Budget Used             12.4%

Expense Details
────────────────────────────

Date        Category       Amount
2026-07-24  Education      ₹2,500
2026-07-08  Food            ₹500
2026-07-08  Shopping       ₹1,200
2026-07-08  Travel          ₹700
2026-07-08  Healthcare     ₹1,300
```

The actual report values depend on the user's stored financial data.

---

# 🔒 Security

FinSight follows basic application security practices including:

- Password hashing
- Session-based authentication
- Environment variables for secrets
- User-specific financial records
- Server-side validation
- Protected routes
- Database credentials kept outside source code

Sensitive configuration values should never be committed to GitHub.

---

# 🧪 Testing

Before deployment, the following application flows should be tested.

## Authentication

- Registration
- Login
- Logout
- Invalid credentials
- Password validation

## Expenses

- Add expense
- View expenses
- Edit expense
- Delete expense
- Category filtering

## Budget

- Create budget
- Track budget utilization
- Overspending alerts

## Investments

- Add investment
- View portfolio
- Calculate returns
- Portfolio analytics

## Goals

- Create financial goal
- Add contributions
- Track progress

## Reports

- Generate PDF
- Generate Excel
- Download reports

## Deployment

- Database connectivity
- Environment variables
- Production routes
- Static files
- Authentication

---

# 📈 Project Highlights

- Full-stack Flask web application
- MySQL relational database
- User authentication and authorization
- Personal expense management
- Income tracking
- Budget tracking
- Investment portfolio tracking
- Financial goal planning
- Pandas and NumPy based analytics
- Financial health scoring
- Interactive dashboards
- PDF report generation
- Excel report generation
- Notification and alert system
- Cloud database integration
- Production deployment using Render
- Aiven cloud MySQL database

---

# 📌 Current Scope

The current system focuses on:

- Personal finance management
- Manual financial data entry
- Expense tracking
- Income tracking
- Budget management
- Investment tracking
- Financial goals
- Analytics
- Financial health scoring
- Notifications
- PDF reporting
- Excel reporting
- Cloud database integration
- Web-based financial dashboard

---

# 🔮 Future Scope

FinSight can be extended with:

- Live bank account integration
- UPI transaction integration
- Automated transaction synchronization
- Multi-user family accounts
- Native Android/iOS applications
- Machine learning based expense forecasting
- Advanced investment prediction
- Multi-currency support
- Automated financial recommendations
- AI-powered financial assistant
- Real-time market data integration


---

# 🧰 Development Tools

The project was developed using:

- Python
- Flask
- MySQL
- HTML
- CSS
- JavaScript
- Pandas
- NumPy
- Chart.js
- ReportLab
- OpenPyXL
- Git
- GitHub
- VS Code
- Render
- Aiven

---

# 👩‍💻 Author

## Kinjal Gupta

**B.Tech Computer Science & Engineering**

**SRM Institute of Science and Technology**

### GitHub

[https://github.com/KinjalGupta46](https://github.com/KinjalGupta46)

---

# ⭐ Acknowledgement

This project was developed as part of the **Infosys Springboard Internship Program**.

The project focuses on applying full-stack development, database management, data analytics, and financial technology concepts to build a practical personal finance management platform.

---

# 📜 License

This project is intended for **educational and portfolio purposes**.