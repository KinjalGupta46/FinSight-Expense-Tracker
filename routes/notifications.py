from flask import Blueprint, render_template, session, redirect
from database import mysql

notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("/notifications")
def notifications():

    if "user_id" not in session:
        return redirect("/login")

    cursor = mysql.connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            title,
            message,
            type,
            is_read,
            created_at
        FROM notifications
        WHERE user_id=%s
        ORDER BY created_at DESC
    """, (session["user_id"],))

    notifications = cursor.fetchall()

    cursor.close()

    return render_template(
        "notifications.html",
        notifications=notifications
    )


@notifications_bp.route("/notifications/read/<int:id>")
def mark_notification_read(id):

    if "user_id" not in session:
        return redirect("/login")

    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE notifications
        SET is_read=1
        WHERE id=%s
        AND user_id=%s
    """, (id, session["user_id"]))

    mysql.connection.commit()

    cursor.close()

    return redirect("/notifications")