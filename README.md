## Flask Blog App

An educational Flask web application implementing user authentication, PostgreSQL persistence, and CRUD over a main domain entity with URL slugs. Built to satisfy the project rubric.

### Domain
Blog posts created by registered users.

### Requirements
- Python >= 3.12
- Flask >= 3.1.2
- Flask-WTF >= 1.2.2
- Flask-Login >= 0.6.3
- Flask-SQLAlchemy >= 3.1.1
- PostgreSQL (psycopg >= 3.2.10)
- python-slugify >= 8.0.4
- email-validator >= 2.3.0

### Setup with Rye
1. Install Rye: see `https://rye-up.com/`.
2. From repo root:
```
rye sync
```

### Environment
Create a `.env` file (or set environment vars) with:
```
FLASK_SECRET_KEY="123456789"
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/flask_blog
```

Env variables reference:
- `FLASK_SECRET_KEY`: cryptographically strong random string for sessions/CSRF.
- `DATABASE_URL`: SQLAlchemy URL for PostgreSQL in the form `postgresql+psycopg://user:password@host:port/dbname`.
- `FLASK_ENV`: optional, `development` enables debug features.

### Database
Create a PostgreSQL database named `flask_blog` (or adjust `DATABASE_URL`).
You can use the helper script:
```
powershell -ExecutionPolicy Bypass -File scripts/create_db.ps1 -AdminUser postgres
```

### Run
```
rye run dev
```
Briefly, to run the project, the following commands must be used in this order:
```
- git clone https://github.com/Jre321/Blog-Web.git
- cd .\Blog-Web\
- rye sync
- $env:FLASK_SECRET_KEY = "123456789"
$env:DATABASE_URL = "postgresql+psycopg://flaskuser:flaskpass@localhost:5432/flask_blog"
- rye run dev
```
