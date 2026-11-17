
from flask import Blueprint, request, render_template_string

events_bp = Blueprint("events", __name__)

# Sample approved events
EVENTS = [
    {
        "id": 1,
        "name": "Summer Music Festival",
        "category": "Music",
        "date": "15 December 2026",
        "time": "6:00 PM",
        "location": "Colombo",
        "price": "LKR 2,500",
        "description": "Enjoy live music, talented artists and amazing performances.",
        "image": "https://images.unsplash.com/photo-1506157786151-b8491531f063?w=700"
    },
    {
        "id": 2,
        "name": "Tech Innovation Summit",
        "category": "Technology",
        "date": "20 December 2026",
        "time": "9:00 AM",
        "location": "Kandy",
        "price": "LKR 1,500",
        "description": "Explore technology, innovation and future opportunities.",
        "image": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=700"
    },
    {
        "id": 3,
        "name": "Business Networking Event",
        "category": "Business",
        "date": "25 December 2026",
        "time": "10:00 AM",
        "location": "Jaffna",
        "price": "LKR 1,000",
        "description": "Connect with professionals and share business ideas.",
        "image": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=700"
    },
    {
        "id": 4,
        "name": "Web Development Workshop",
        "category": "Education",
        "date": "28 December 2026",
        "time": "9:00 AM",
        "location": "Vavuniya",
        "price": "LKR 800",
        "description": "Learn modern web development technologies.",
        "image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=700"
    },
    {
        "id": 5,
        "name": "New Year Music Night",
        "category": "Music",
        "date": "31 December 2026",
        "time": "7:00 PM",
        "location": "Colombo",
        "price": "LKR 3,000",
        "description": "Celebrate the new year with music and entertainment.",
        "image": "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=700"
    }
]


@events_bp.route("/events")
def events():

    search = request.args.get("search", "").strip().lower()
    category = request.args.get("category", "All")

    # Display approved sample events only
    approved_events = EVENTS.copy()

    filtered_events = [
        event for event in approved_events
        if search in event["name"].lower()
        and (category == "All" or event["category"] == category)
    ]

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>EventGo | All Events</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
* { box-sizing:border-box; margin:0; padding:0; }

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

.logo { color:#5594ff; font-size:25px; font-weight:bold; }

a { text-decoration:none; color:inherit; }

.container { padding:55px 8%; }

h1 { margin-bottom:15px; }

.subtitle { color:#aabbd2; margin-bottom:30px; }

form {
    display:flex;
    gap:12px;
    margin-bottom:35px;
    flex-wrap:wrap;
}

input, select {
    padding:13px;
    border-radius:7px;
    border:1px solid #29466d;
    background:#102441;
    color:white;
}

input { flex:1; min-width:180px; }

button, .btn {
    background:#2869e8;
    border:0;
    padding:13px 22px;
    color:white;
    border-radius:7px;
    cursor:pointer;
}

.grid {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:25px;
}

.card {
    background:#102441;
    border:1px solid #243d60;
    border-radius:12px;
    overflow:hidden;
}

.card img {
    width:100%;
    height:190px;
    object-fit:cover;
}

.content { padding:20px; }

.content p {
    color:#b8c7dc;
    margin:12px 0;
    font-size:14px;
}

.btn { display:inline-block; }

@media(max-width:800px) {
    .grid { grid-template-columns:repeat(2,1fr); }
}

@media(max-width:550px) {
    .grid { grid-template-columns:1fr; }
}
</style>
</head>

<body>

<nav>
    <div class="logo">EventGo.</div>
    <div>
        <a href="/">Home</a> &nbsp;&nbsp;
        <a href="/login">Login</a>
    </div>
</nav>

<div class="container">

<h1>Explore All Events</h1>
<p class="subtitle">Discover events and find your next experience.</p>

<form method="GET" action="/events">

    <input
        type="text"
        name="search"
        placeholder="Search events..."
        value="{{ search }}"
    >

    <select name="category">
        {% for cat in categories %}
        <option value="{{ cat }}"
            {% if category == cat %}selected{% endif %}>
            {{ cat }}
        </option>
        {% endfor %}
    </select>

    <button type="submit">Search</button>

    <a href="/events" class="btn">Reset</a>

</form>

<div class="grid">

{% for event in events %}

<div class="card">

    <img src="{{ event.image }}" alt="{{ event.name }}">

    <div class="content">

        <h3>{{ event.name }}</h3>

        <p>Category: {{ event.category }}</p>
        <p>Date: {{ event.date }}</p>
        <p>Location: {{ event.location }}</p>
        <p>Ticket: {{ event.price }}</p>

        <a href="/event/{{ event.id }}" class="btn">
            View Details
        </a>

    </div>
</div>

{% else %}

<p>No events found. Try another search.</p>

{% endfor %}

</div>
</div>

</body>
</html>
""",
        events=filtered_events,
        search=search,
        category=category,
        categories=["All", "Music", "Technology", "Business", "Education"]
    )
