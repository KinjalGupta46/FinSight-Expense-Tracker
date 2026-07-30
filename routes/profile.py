from flask import Flask
from config import Config
from database import mysql

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.expense import expense_bp
from routes.budget import budget_bp
from routes.profile import profile_bp

app = Flask(__name__)
app.config.from_object(Config)

mysql.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(expense_bp)
app.register_blueprint(budget_bp)
app.register_blueprint(profile_bp)

if __name__ == "__main__":
    app.run(debug=True)