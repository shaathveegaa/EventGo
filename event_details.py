
from flask import Blueprint, render_template_string, abort, session, redirect, url_for
from events import EVENTS

details_bp = Blueprint("details", __name__)


@details_bp.route("/event/<int:event_id>")
def event_details(event_id):

    event = next(
        (e for e in EVENTS if e["id"] == event_id),
        None
    )

    if event is None:
        abort(404)

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>EventGo | Event Details</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
* {
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body {
    background:#07152b;
    color:white;
    font-family:Poppins,sans-serif;
}

nav {
    background:#0b1d38;
    padding:22px 8%;
    display:flex;
    justify-content:space-between;
}

.logo {
    font-size:25px;
    font-weight:bold;
    color:#5594ff;
}

a {
    color:white;
    text-decoration:none;
}

.container {
    max-width:1000px;
    margin:50px auto;
    padding:20px;
}

.event-image {
    width:100%;
    height:400px;
    object-fit:cover;
    border-radius:15px;
}

.details {
    background:#102441;
    padding:30px;
    margin-top:25px;
    border-radius:12px;
    border:1px solid #243d60;
}

h1 {
    margin-bottom:15px;
}

p {
    color:#bdcce0;
    margin:15px 0;
    line-height:1.8;
}

.info {
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:15px;
    margin:25px 0;
}

.info div {
    background:#172e4d;
    padding:15px;
    border-radius:8px;
}

.price {
    color:#62a0ff;
    font-size:23px;
    font-weight:bold;
}

.btn {
    display:inline-block;
    background:#2869e8;
    padding:14px 28px;
    border-radius:8px;
    margin-top:15px;
}

.btn:hover {
    background:#4384ff;
}

@media(max-width:600px) {
    .event-image { height:230px; }
    .info { grid-template-columns:1fr; }
}
</style>
</head>

<body>

<nav>
    <div class="logo">EventGo.</div>
    <div>
        <a href="/">Home</a> &nbsp;&nbsp;
        <a href="/events">Events</a>
    </div>
</nav>

<div class="container">

    <img src="{{ event.image }}"
         alt="{{ event.name }}"
         class="event-image">

    <div class="details">

        <h1>{{ event.name }}</h1>

        <p>{{ event.description }}</p>

        <div class="info">

            <div>
                <strong>Category</strong>
                <p>{{ event.category }}</p>
            </div>

            <div>
                <strong>Date</strong>
                <p>{{ event.date }}</p>
            </div>

            <div>
                <strong>Time</strong>
                <p>{{ event.time }}</p>
            </div>

            <div>
                <strong>Location</strong>
                <p>{{ event.location }}</p>
            </div>

        </div>

        <p class="price">Ticket Price: {{ event.price }}</p>

        {% if session.get("user_id") %}
            <a href="/book/{{ event.id }}" class="btn">
                Book Now
            </a>
        {% else %}
            <a href="/login?next=/book/{{ event.id }}" class="btn">
                Login to Book
            </a>
        {% endif %}

    </div>

</div>

</body>
</html>
""", event=event)


@details_bp.route("/book/<int:event_id>")
def book_event(event_id):

    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    event = next(
        (e for e in EVENTS if e["id"] == event_id),
        None
    )

    if event is None:
        abort(404)

    if session.get("role") != "customer":
        return "Only customer accounts can book events.", 403

    return render_template_string("""
    <body style="
        background:#07152b;
        color:white;
        font-family:Arial;
        text-align:center;
        padding:100px 20px;
    ">
        <h1>Booking Module</h1>
        <h2>{{ event.name }}</h2>
        <p>Welcome, {{ session.get('username') }}!</p>
        <p>Booking functionality will be implemented in the next module.</p>
        <a href="/events" style="color:#5594ff;">Back to Events</a>
    </body>
    """, event=event)
