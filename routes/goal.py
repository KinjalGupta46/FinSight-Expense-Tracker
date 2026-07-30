from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import mysql

goal_bp = Blueprint("goal", __name__)


# -------------------- Add Goal -------------------- #
@goal_bp.route("/add-goal", methods=["GET", "POST"])
def add_goal():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        goal_name = request.form["goal_name"]
        target_amount = float(request.form["target_amount"])
        saved_amount = float(request.form["saved_amount"])
        deadline = request.form["deadline"]

        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO financial_goals
            (user_id, goal_name, target_amount, saved_amount, deadline)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            session["user_id"],
            goal_name,
            target_amount,
            saved_amount,
            deadline
        ))

        mysql.connection.commit()
        cursor.close()

        flash("Financial Goal Added Successfully!", "success")

        return redirect(url_for("goal.view_goals"))

    return render_template("add_goal.html")


# -------------------- View Goals -------------------- #
@goal_bp.route("/goals")
def view_goals():

    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor = mysql.connection.cursor()

    # Fetch all goals
    cursor.execute("""
        SELECT
            id,
            goal_name,
            target_amount,
            saved_amount,
            deadline
        FROM financial_goals
        WHERE user_id=%s
        ORDER BY id DESC
    """, (session["user_id"],))

    goals = cursor.fetchall()

    # Summary
    cursor.execute("""
        SELECT
            COUNT(*),
            IFNULL(SUM(target_amount),0),
            IFNULL(SUM(saved_amount),0)
        FROM financial_goals
        WHERE user_id=%s
    """, (session["user_id"],))

    summary = cursor.fetchone()

    total_goals = summary[0]
    total_target = float(summary[1])
    total_saved = float(summary[2])

    remaining_amount = total_target - total_saved

    if total_target > 0:
        overall_progress = round((total_saved / total_target) * 100, 2)
    else:
        overall_progress = 0

    completed_goals = 0

    for goal in goals:
        if float(goal[3]) >= float(goal[2]):
            completed_goals += 1

    cursor.close()

    return render_template(
        "goals.html",
        goals=goals,
        total_goals=total_goals,
        total_target=total_target,
        total_saved=total_saved,
        remaining_amount=remaining_amount,
        completed_goals=completed_goals,
        overall_progress=overall_progress
    )


# -------------------- Delete Goal -------------------- #
@goal_bp.route("/delete-goal/<int:id>")
def delete_goal(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor = mysql.connection.cursor()

    cursor.execute("""
        DELETE FROM financial_goals
        WHERE id=%s AND user_id=%s
    """, (
        id,
        session["user_id"]
    ))

    mysql.connection.commit()
    cursor.close()

    flash("Goal Deleted Successfully!", "success")

    return redirect(url_for("goal.view_goals"))


# -------------------- Edit Goal -------------------- #
@goal_bp.route("/edit-goal/<int:id>", methods=["GET", "POST"])
def edit_goal(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    cursor = mysql.connection.cursor()

    if request.method == "POST":

        goal_name = request.form["goal_name"]
        target_amount = float(request.form["target_amount"])
        saved_amount = float(request.form["saved_amount"])
        deadline = request.form["deadline"]

        cursor.execute("""
            UPDATE financial_goals
            SET
                goal_name=%s,
                target_amount=%s,
                saved_amount=%s,
                deadline=%s
            WHERE id=%s
            AND user_id=%s
        """, (
            goal_name,
            target_amount,
            saved_amount,
            deadline,
            id,
            session["user_id"]
        ))

        mysql.connection.commit()
        cursor.close()

        flash("Goal Updated Successfully!", "success")

        return redirect(url_for("goal.view_goals"))

    cursor.execute("""
        SELECT
            goal_name,
            target_amount,
            saved_amount,
            deadline
        FROM financial_goals
        WHERE id=%s
        AND user_id=%s
    """, (
        id,
        session["user_id"]
    ))

    goal = cursor.fetchone()

    cursor.close()

    return render_template(
        "edit_goal.html",
        goal=goal
    )