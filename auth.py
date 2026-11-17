
import sqlite3
from functools import wraps
from flask import (
    Blueprint, request, render_template_string,
    redirect, url_for, session, flash
)
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

DB_NAME = "eventgo.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'customer'
        )
    """)

    conn.commit()
    conn.close()


# Role-based access decorator
def role_required(*allowed_roles):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if not session.get("user_id"):
                return redirect(url_for("auth.login"))

            if session.get("role") not in allowed_roles:
                return "Access denied: You do not have permission.", 403

            return func(*args, **kwargs)

        return wrapper

    return decorator


# Registration page
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not password:
            return "Please fill in all required fields.", 400

        if password != confirm_password:
            return "Passwords do not match.", 400

        if len(password) < 8:
            return "Password must contain at least 8 characters.", 400

        hashed_password = generate_password_hash(password)

        conn = get_db()

        try:

            conn.execute("""
                INSERT INTO users (name, email, password, role)
                VALUES (?, ?, ?, 'customer')
            """, (name, email, hashed_password))

            conn.commit()

            conn.close()

            return redirect(url_for("auth.login"))

        except sqlite3.IntegrityError:

            conn.close()
            return "This email is already registered.", 400

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>EventGo | Register</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
* {
    box-sizing:border-box;
}

body {
    margin:0;
    background:#07152b;
    color:white;
    font-family:Arial,sans-serif;
    display:flex;
    justify-content:center;
    align-items:center;
    min-height:100vh;
}

.container {
    background:#102441;
    padding:40px;
    width:90%;
    max-width:430px;
    border-radius:15px;
    border:1px solid #29466d;
}

h1 {
    color:#5594ff;
    text-align:center;
}

p {
    color:#b8c7dc;
    text-align:center;
}

input {
    width:100%;
    padding:14px;
    margin:10px 0;
    background:#07152b;
    border:1px solid #29466d;
    color:white;
    border-radius:7px;
}

button {
    width:100%;
    padding:14px;
    background:#2869e8;
    border:0;
    color:white;
    border-radius:7px;
    cursor:pointer;
    margin-top:15px;
}

a {
    color:#5594ff;
    text-decoration:none;
}
</style>
</head>

<body>

<div class="container">

    <h1>EventGo.</h1>
    <p>Create your customer account</p>

    <form method="POST">

        <input type="text" name="name"
               placeholder="Full Name" required>

        <input type="email" name="email"
               placeholder="Email Address" required>

        <input type="password" name="password"
               placeholder="Password (minimum 8 characters)" required>

        <input type="password" name="confirm_password"
               placeholder="Confirm Password" required>

        <button type="submit">Create Account</button>

    </form>

    <p>Already have an account?
        <a href="/login">Login</a>
    </p>

    <p><a href="/">Back to Home</a></p>

</div>

</body>
</html>
""")


# Login page
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        next_url = request.form.get("next", "/")

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session.clear()

            session["user_id"] = user["id"]
            session["username"] = user["name"]
            session["role"] = user["role"]

            # Allow only local application redirects
            if not next_url.startswith("/") or next_url.startswith("//"):
                next_url = "/"

            return redirect(next_url)

        return "Invalid email or password.", 401

    next_url = request.args.get("next", "/")

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>EventGo | Login</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
* {
    box-sizing:border-box;
}

body {
    margin:0;
    background:#07152b;
    color:white;
    font-family:Arial,sans-serif;
    display:flex;
    justify-content:center;
    align-items:center;
    min-height:100vh;
}

.container {
    background:#102441;
    padding:40px;
    width:90%;
    max-width:430px;
    border-radius:15px;
    border:1px solid #29466d;
}

h1 {
    color:#5594ff;
    text-align:center;
}

p {
    color:#b8c7dc;
    text-align:center;
}

input {
    width:100%;
    padding:14px;
    margin:12px 0;
    background:#07152b;
    border:1px solid #29466d;
    color:white;
    border-radius:7px;
}

button {
    width:100%;
    padding:14px;
    background:#2869e8;
    border:0;
    color:white;
    border-radius:7px;
    cursor:pointer;
}

a {
    color:#5594ff;
    text-decoration:none;
}
</style>
</head>

<body>

<div class="container">

    <h1>EventGo.</h1>
    <p>Welcome back! Login to continue.</p>

    <form method="POST">

        <input type="hidden" name="next"
               value="{{ next_url }}">

        <input type="email" name="email"
               placeholder="Email Address" required>

        <input type="password" name="password"
               placeholder="Password" required>

        <button type="submit">Login</button>

    </form>

    <p>Don't have an account?
        <a href="/register">Register</a>
    </p>

    <p><a href="/">Back to Home</a></p>

</div>

</body>
</html>
""", next_url=next_url)


# Logout
@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# Customer dashboard
@auth_bp.route("/customer/dashboard")
@role_required("customer")
def customer_dashboard():

    return f"""
    <body style="background:#07152b;color:white;
                 font-family:Arial;text-align:center;padding:80px">
        <h1>Customer Dashboard</h1>
        <h2>Welcome {session.get('username')}!</h2>
        <p>You are logged in as a customer.</p>
        <a href="/events" style="color:#5594ff;">Explore Events</a>
        <br><br>
        <a href="/logout" style="color:#5594ff;">Logout</a>
    </body>
    """


# Organizer dashboard
@auth_bp.route("/organizer/dashboard")
@role_required("organizer")
def organizer_dashboard():

    return """
    <body style="background:#07152b;color:white;
                 font-family:Arial;text-align:center;padding:80px">
        <h1>Organizer Dashboard</h1>
        <p>Manage your events here.</p>
        <a href="/logout" style="color:#5594ff;">Logout</a>
    </body>
    """


# Admin dashboard
@auth_bp.route("/admin/dashboard")
@role_required("admin")
def admin_dashboard():

    return """
    <body style="background:#07152b;color:white;
                 font-family:Arial;text-align:center;padding:80px">
        <h1>Admin Dashboard</h1>
        <p>Manage users, events and approvals here.</p>
        <a href="/logout" style="color:#5594ff;">Logout</a>
    </body>
    """
