from flask import Flask, render_template, request, redirect, session, jsonify
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required, get_db, validate_date
import sqlite3
from datetime import datetime, date, timedelta
import json
from functools import wraps

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def dict_factory(cursor, row):
    """Convert database row objects to dictionaries"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Homepage/Dashboard
@app.route("/")
@login_required
def index():
    """Show dashboard with today's habits"""
    db = get_db()
    db.row_factory = dict_factory
    today = date.today().isoformat()

    # Get user's habits
    habits_raw = db.execute("""
        SELECT h.*,
               (SELECT COUNT(*) FROM completions
                WHERE habit_id = h.id AND date = ? AND completed = 1) as today_completed,
               (SELECT COUNT(*) FROM completions
                WHERE habit_id = h.id AND completed = 1) as total_completed,
               (SELECT COUNT(*) FROM completions
                WHERE habit_id = h.id AND date >= date('now', '-30 days')) as recent_checks
        FROM habits h
        WHERE h.user_id = ?
        ORDER BY h.name
    """, (today, session["user_id"])).fetchall()

    # Convert to list of dictionaries and calculate streaks
    habits = []
    for habit in habits_raw:
        habit_dict = dict(habit)
        streak = calculate_streak(db, habit_dict["id"])
        habit_dict["streak"] = streak
        habits.append(habit_dict)

    # Get completion rate for last 7 days
    completion_rate = {}
    for i in range(6, -1, -1):
        day = (date.today() - timedelta(days=i)).isoformat()
        completed = db.execute("""
            SELECT COUNT(*) as count FROM completions c
            JOIN habits h ON c.habit_id = h.id
            WHERE h.user_id = ? AND c.date = ? AND c.completed = 1
        """, (session["user_id"], day)).fetchone()["count"]

        total = db.execute("""
            SELECT COUNT(*) as count FROM habits
            WHERE user_id = ?
        """, (session["user_id"],)).fetchone()["count"]

        rate = (completed / total * 100) if total > 0 else 0
        completion_rate[day] = round(rate)

    return render_template("index.html", habits=habits, today=today,
                          completion_rate=json.dumps(completion_rate))

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("login.html", error="Must provide username and password")

        db = get_db()
        db.row_factory = dict_factory
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if not user or not check_password_hash(user["hash"], password):
            return render_template("login.html", error="Invalid username/password")

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect("/")

    return render_template("login.html")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate
        if not username or not password or not confirmation:
            return render_template("register.html", error="All fields are required")

        if password != confirmation:
            return render_template("register.html", error="Passwords do not match")

        if len(password) < 6:
            return render_template("register.html", error="Password must be at least 6 characters")

        db = get_db()
        db.row_factory = dict_factory

        # Check if username exists
        existing = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        if existing:
            return render_template("register.html", error="Username already exists")

        # Insert new user
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))
        db.commit()

        # Log in automatically
        user = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        session["user_id"] = user["id"]
        session["username"] = username

        return redirect("/")

    return render_template("register.html")

# Logout
@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/login")

# Manage Habits
@app.route("/habits", methods=["GET", "POST"])
@login_required
def manage_habits():
    """Add, edit, or delete habits"""
    db = get_db()
    db.row_factory = dict_factory

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            name = request.form.get("name")
            color = request.form.get("color", "#4CAF50")
            frequency = request.form.get("frequency", "daily")

            if not name:
                return render_template("habits.html", error="Habit name is required")

            db.execute("""
                INSERT INTO habits (user_id, name, color, frequency)
                VALUES (?, ?, ?, ?)
            """, (session["user_id"], name, color, frequency))
            db.commit()

        elif action == "delete":
            habit_id = request.form.get("habit_id")
            if habit_id:
                db.execute("DELETE FROM habits WHERE id = ? AND user_id = ?",
                          (habit_id, session["user_id"]))
                db.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
                db.commit()

        elif action == "edit":
            habit_id = request.form.get("habit_id")
            name = request.form.get("name")
            color = request.form.get("color")
            frequency = request.form.get("frequency")

            if habit_id and name:
                db.execute("""
                    UPDATE habits
                    SET name = ?, color = ?, frequency = ?
                    WHERE id = ? AND user_id = ?
                """, (name, color, frequency, habit_id, session["user_id"]))
                db.commit()

        return redirect("/habits")

    # GET request - show all habits
    habits = db.execute("""
        SELECT * FROM habits
        WHERE user_id = ?
        ORDER BY name
    """, (session["user_id"],)).fetchall()

    return render_template("habits.html", habits=habits)

# Toggle Habit Completion (API endpoint)
@app.route("/toggle", methods=["POST"])
@login_required
def toggle_completion():
    """Toggle habit completion for today"""
    habit_id = request.form.get("habit_id")
    completed = request.form.get("completed")
    custom_date = request.form.get("date")

    if not habit_id:
        return jsonify({"error": "Missing habit_id"}), 400

    # Validate user owns this habit
    db = get_db()
    db.row_factory = dict_factory
    habit = db.execute("SELECT id FROM habits WHERE id = ? AND user_id = ?",
                      (habit_id, session["user_id"])).fetchone()
    if not habit:
        return jsonify({"error": "Habit not found"}), 404

    # Use today or custom date
    check_date = custom_date if custom_date else date.today().isoformat()

    # Check if entry exists
    existing = db.execute("""
        SELECT * FROM completions
        WHERE habit_id = ? AND date = ?
    """, (habit_id, check_date)).fetchone()

    if existing:
        # Update existing
        db.execute("""
            UPDATE completions
            SET completed = ?
            WHERE habit_id = ? AND date = ?
        """, (1 if completed == "true" else 0, habit_id, check_date))
    else:
        # Insert new
        db.execute("""
            INSERT INTO completions (habit_id, date, completed, notes)
            VALUES (?, ?, ?, '')
        """, (habit_id, check_date, 1 if completed == "true" else 0))

    db.commit()

    # Calculate new streak
    streak = calculate_streak(db, habit_id)

    return jsonify({
        "success": True,
        "streak": streak,
        "date": check_date
    })

# Calendar View
@app.route("/calendar")
@login_required
def calendar_view():
    """Show monthly calendar view"""
    year = request.args.get("year", type=int, default=date.today().year)
    month = request.args.get("month", type=int, default=date.today().month)

    # Get first day of month
    first_day = date(year, month, 1)
    # Get last day of month
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)

    db = get_db()
    db.row_factory = dict_factory
    habits = db.execute("""
        SELECT * FROM habits
        WHERE user_id = ?
        ORDER BY name
    """, (session["user_id"],)).fetchall()

    completions = db.execute("""
        SELECT c.habit_id, c.date, c.completed
        FROM completions c
        JOIN habits h ON c.habit_id = h.id
        WHERE h.user_id = ? AND c.date >= ? AND c.date <= ?
    """, (session["user_id"], first_day.isoformat(), last_day.isoformat())).fetchall()

    completion_dict = {}
    for comp in completions:
        if comp["date"] not in completion_dict:
            completion_dict[comp["date"]] = {}
        completion_dict[comp["date"]][comp["habit_id"]] = comp["completed"]

    # Calculate days in month
    days_in_month = []
    current = first_day
    while current <= last_day:
        days_in_month.append({
            "date": current,
            "iso_date": current.isoformat(),
            "weekday": current.weekday(),  # 0=Monday, 6=Sunday
            "completions": completion_dict.get(current.isoformat(), {})
        })
        current += timedelta(days=1)

    # Navigation for previous/next month
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    return render_template("calendar.html",
                          year=year, month=month,
                          days=days_in_month, habits=habits,
                          prev_year=prev_year, prev_month=prev_month,
                          next_year=next_year, next_month=next_month,
                          month_name=first_day.strftime("%B"))

# Statistics
@app.route("/statistics")
@login_required
def statistics():
    """Show habit statistics"""
    db = get_db()
    db.row_factory = dict_factory

    habits_raw = db.execute("""
        SELECT h.*,
               COUNT(CASE WHEN c.completed = 1 THEN 1 END) as completed_count,
               COUNT(c.id) as total_checks,
               MAX(c.date) as last_check
        FROM habits h
        LEFT JOIN completions c ON h.id = c.habit_id
        WHERE h.user_id = ?
        GROUP BY h.id
        ORDER BY h.name
    """, (session["user_id"],)).fetchall()


    habits = []
    best_habit = None
    worst_habit = None
    best_rate = -1
    worst_rate = 101

    for habit in habits_raw:
        habit_dict = dict(habit)
        habit_dict["completion_rate"] = round((habit_dict["completed_count"] / habit_dict["total_checks"] * 100), 1) if habit_dict["total_checks"] > 0 else 0
        habit_dict["streak"] = calculate_streak(db, habit_dict["id"])

        # Track best and worst habits
        rate = habit_dict["completion_rate"]
        if rate > best_rate:
            best_rate = rate
            best_habit = habit_dict
        if rate < worst_rate:
            worst_rate = rate
            worst_habit = habit_dict

        habits.append(habit_dict)


    daily_data = []
    for i in range(29, -1, -1):
        day = (date.today() - timedelta(days=i)).isoformat()
        completed_result = db.execute("""
            SELECT COUNT(*) as count FROM completions c
            JOIN habits h ON c.habit_id = h.id
            WHERE h.user_id = ? AND c.date = ? AND c.completed = 1
        """, (session["user_id"], day)).fetchone()
        completed = completed_result["count"] if completed_result else 0

        total_result = db.execute("""
            SELECT COUNT(*) as count FROM habits
            WHERE user_id = ?
        """, (session["user_id"],)).fetchone()
        total = total_result["count"] if total_result else 0

        rate = round((completed / total * 100), 1) if total > 0 else 0
        daily_data.append({
            "date": day,
            "completed": completed,
            "total": total,
            "rate": rate
        })

    avg_rate = round(sum(h["completion_rate"] for h in habits) / len(habits), 1) if habits else 0

    return render_template("statistics.html",
                          habits=habits,
                          daily_data=daily_data,
                          best_habit=best_habit,
                          worst_habit=worst_habit,
                          avg_rate=avg_rate)


def calculate_streak(db, habit_id):
    """Calculate current streak for a habit"""

    db.row_factory = dict_factory
    completions = db.execute("""
        SELECT date, completed
        FROM completions
        WHERE habit_id = ?
        ORDER BY date DESC
    """, (habit_id,)).fetchall()

    streak = 0
    current_date = date.today()

    for comp in completions:
        comp_date = datetime.strptime(comp["date"], "%Y-%m-%d").date()

        if comp_date <= current_date and comp["completed"] == 1:
            if streak == 0:
                # First completed day found
                streak = 1
                current_date = comp_date - timedelta(days=1)
            elif comp_date == current_date:
                streak += 1
                current_date = comp_date - timedelta(days=1)
            else:
                # Gap found, break streak
                break
        elif comp["completed"] == 0 and comp_date == date.today():
            streak = 0
            break
        else:
            # Gap found
            break

    return streak

if __name__ == "__main__":
    app.run(debug=True)


# Wrote README.md with deepseek
# made statistics functionality using deepseek
# Took ideas from various projects about color and calendar implementing
