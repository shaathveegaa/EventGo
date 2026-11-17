# 🎟️ EventGo – Event Management and Online Ticket Booking System

EventGo is a web-based event management and online ticket booking platform developed using Python and Flask. It provides a convenient platform for users to discover events, book tickets, and manage their bookings. Organizers can create and manage events, while administrators oversee platform activities.

## 🚀 Project Overview

The main goal of EventGo is to simplify event discovery, event management, and ticket booking through a user-friendly and responsive web application.

## ✨ Features

### 👤 User Management
- User registration and login
- Secure user authentication
- Role-based access control
- Customer, Organizer, and Administrator accounts

### 🎉 Event Management
- Create and manage events
- Browse available events
- Search and filter events
- View event details
- Admin approval for submitted events

### 🎫 Ticket Booking
- Browse available ticket types
- View ticket prices and availability
- Book free and paid tickets
- View booking history
- Generate QR-code tickets
- Download tickets as PDF

### 💳 Payment Management
- Online payment integration using PayHere
- Manage payment transactions
- Track booking payment status

### 🛠️ Administration
- Manage users and organizers
- Approve or reject submitted events
- Monitor bookings and payments
- View platform reports

## 🧰 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| PostgreSQL | Relational database |
| Docker Desktop | Running PostgreSQL in a container |
| HTML5 | Web page structure |
| CSS3 | Styling |
| JavaScript | Frontend interactivity |
| Bootstrap 5 | Responsive user interface |
| Git | Version control |
| GitHub | Source code hosting |

## 🏗️ System Architecture

```text
                 EventGo Website
                       |
                       |
                Flask Application
                  (Python)
                       |
                       |
              PostgreSQL Database
                       |
                Docker Container
                       |
               Persistent Volume
```

PostgreSQL runs inside a Docker container, allowing the database to operate independently without requiring a separate PostgreSQL Server installation on the host computer.

## 📁 Project Structure

```text
EventGo/
│
├── app.py
├── auth.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   └── register.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

*The project structure may change as development progresses.*

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/shaathveegaa/EventGo.git
```

### 2. Navigate to the Project Directory

```bash
cd EventGo
```

### 3. Create a Python Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 5. Install and Start Docker Desktop

Install Docker Desktop and make sure Docker Engine is running.

Official website: https://www.docker.com/products/docker-desktop/

### 6. Run PostgreSQL Using Docker

Execute the following command in the VS Code terminal:

```powershell
docker run --name eventgo-db `
  -e POSTGRES_USER=eventgo_user `
  -e POSTGRES_PASSWORD=your_password `
  -e POSTGRES_DB=eventgo_db `
  -p 5432:5432 `
  -v eventgo_postgres_data:/var/lib/postgresql/data `
  -d postgres:17
```

This command:

- Downloads the PostgreSQL 17 Docker image if needed.
- Creates a PostgreSQL container named `eventgo-db`.
- Creates a database named `eventgo_db`.
- Creates a database user named `eventgo_user`.
- Stores database data in a persistent Docker volume.

### 7. Verify the PostgreSQL Container

```powershell
docker ps
```

To access the PostgreSQL database:

```powershell
docker exec -it eventgo-db psql -U eventgo_user -d eventgo_db
```

### 8. Configure Environment Variables

Create a `.env` file in the project root directory.

```env
DB_HOST=localhost
DB_NAME=eventgo_db
DB_USER=eventgo_user
DB_PASSWORD=your_password
DB_PORT=5432
```

Use the same password configured in the Docker command.

**Important:** Never upload your `.env` file or actual database credentials to GitHub.

### 9. Run the Flask Application

```powershell
python app.py
```

Open your browser and visit:

http://127.0.0.1:5001

## 🔐 Security

- Secure password hashing
- Environment variables for sensitive configuration
- Role-based access control
- Protected application routes
- Secure handling of payment credentials

## 📌 Project Status

🚧 **Under Development**

EventGo is currently under development. New features and improvements will be added throughout the development process.

## 👩‍💻 Developer

**Shaathveegaa Rajeshkannan**

- GitHub: [@shaathveegaa](https://github.com/shaathveegaa)
- Project Repository: [EventGo](https://github.com/shaathveegaa/EventGo)

---

⭐ Thank you for visiting EventGo!

