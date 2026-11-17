
from flask import Flask, render_template_string
from events import events_bp, EVENTS
from event_details import details_bp
from auth import auth_bp, init_db

app = Flask(__name__)
app.secret_key = "eventgo_secret_key_change_later"

# Connect the separate page modules
app.register_blueprint(events_bp)
app.register_blueprint(details_bp)
app.register_blueprint(auth_bp)

# Create authentication database
init_db()


@app.route("/")
def home():

    featured = EVENTS[:3]
    upcoming = EVENTS[3:]

    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EventGo | Discover Events</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Poppins', sans-serif;
    background: #07152b;
    color: white;
}

a {
    text-decoration: none;
    color: inherit;
}

nav {
    height: 80px;
    padding: 0 8%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #0b1d38;
    border-bottom: 1px solid #203657;
}

.logo {
    font-size: 27px;
    font-weight: 800;
    color: #4c8dff;
}

.nav-links {
    display: flex;
    gap: 30px;
    align-items: center;
}

.nav-links a {
    color: #cbd5e1;
    font-size: 14px;
}

.nav-links a:hover {
    color: #4c8dff;
}

.btn {
    background: #2869e8;
    color: white;
    padding: 12px 24px;
    border-radius: 8px;
    display: inline-block;
}

.btn:hover {
    background: #4384ff;
}

.hero {
    min-height: 470px;
    padding: 100px 8%;
    background: linear-gradient(120deg, #0b1d38, #102e5c);
}

.hero h1 {
    font-size: 48px;
    max-width: 650px;
    line-height: 1.3;
}

.hero h1 span {
    color: #5594ff;
}

.hero p {
    color: #b8c7dc;
    margin: 20px 0 30px;
    max-width: 550px;
    line-height: 1.8;
}

section {
    padding: 65px 8%;
}

.section-title {
    font-size: 28px;
    margin-bottom: 30px;
}

.cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
}

.event-card {
    background: #102441;
    border: 1px solid #243d60;
    border-radius: 13px;
    overflow: hidden;
    transition: .3s;
}

.event-card:hover {
    transform: translateY(-7px);
    border-color: #4384ff;
}

.event-card img {
    width: 100%;
    height: 190px;
    object-fit: cover;
}

.card-content {
    padding: 20px;
}

.card-content p {
    color: #aabbd2;
    font-size: 13px;
    margin: 10px 0;
}

.card-content h3 {
    font-size: 18px;
}

.category-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
}

.category {
    background: #102441;
    border: 1px solid #243d60;
    padding: 30px 15px;
    text-align: center;
    border-radius: 12px;
}

.category:hover {
    background: #173763;
}

footer {
    background: #030d1c;
    text-align: center;
    padding: 35px;
    color: #9caec5;
}

@media(max-width: 800px) {
    .cards {
        grid-template-columns: repeat(2, 1fr);
    }
    .category-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .hero h1 {
        font-size: 35px;
    }
}

@media(max-width: 550px) {
    .cards {
        grid-template-columns: 1fr;
    }
    .nav-links {
        gap: 10px;
        font-size: 11px;
    }
    nav {
        padding: 0 4%;
    }
}
</style>
</head>

<body>

<nav>
    <div class="logo">EventGo.</div>

    <div class="nav-links">
        <a href="/">Home</a>
        <a href="/events">Events</a>
        <a href="/login">Login</a>
        <a href="/register" class="btn">Register</a>
    </div>
</nav>

<div class="hero">
    <h1>Discover Amazing <span>Events</span> Around You</h1>

    <p>
        Find exciting events, connect with people and
        experience unforgettable moments with EventGo.
    </p>

    <a href="/events" class="btn">Explore Events →</a>
</div>

<section>
    <h2 class="section-title">Featured Events</h2>

    <div class="cards">
        {% for event in featured %}
        <div class="event-card">
            <img src="{{ event.image }}" alt="{{ event.name }}">

            <div class="card-content">
                <h3>{{ event.name }}</h3>
                <p>{{ event.date }} | {{ event.location }}</p>
                <p>{{ event.price }}</p>
                <a href="/event/{{ event.id }}" class="btn">View Details</a>
            </div>
        </div>
        {% endfor %}
    </div>
</section>

<section style="background:#0b1d38">
    <h2 class="section-title">Upcoming Events</h2>

    <div class="cards">
        {% for event in upcoming %}
        <div class="event-card">
            <img src="{{ event.image }}" alt="{{ event.name }}">

            <div class="card-content">
                <h3>{{ event.name }}</h3>
                <p>{{ event.date }} | {{ event.location }}</p>
                <p>{{ event.price }}</p>
                <a href="/event/{{ event.id }}" class="btn">View Details</a>
            </div>
        </div>
        {% endfor %}
    </div>
</section>

<section>
    <h2 class="section-title">Explore Categories</h2>

    <div class="category-grid">
        <a href="/events?category=Music" class="category">🎵<h3>Music</h3></a>
        <a href="/events?category=Technology" class="category">💻<h3>Technology</h3></a>
        <a href="/events?category=Business" class="category">💼<h3>Business</h3></a>
        <a href="/events?category=Education" class="category">📚<h3>Education</h3></a>
    </div>
</section>

<footer>
    <h2>EventGo.</h2>
    <p>Discover. Connect. Experience.</p>
    <p>© 2026 EventGo. All Rights Reserved.</p>
</footer>

</body>
</html>
""", featured=featured, upcoming=upcoming)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
