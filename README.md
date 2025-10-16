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
FLASK_SECRET_KEY=change-me
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
Or run the SQL directly:
```
psql -U postgres -d postgres -f scripts/create_db.sql
```

### Run
```
rye run dev
```

### Routes
| Method | Path               | Auth | Description                         |
|-------:|--------------------|:----:|-------------------------------------|
| GET    | `/`                |  -   | List posts                          |
| GET    | `/post/<slug>/`    |  -   | Post detail by slug                 |
| GET    | `/login`           |  -   | Render login form                   |
| POST   | `/login`           |  -   | Authenticate user                   |
| GET    | `/signup/`         |  -   | Render signup form                  |
| POST   | `/signup/`         |  -   | Create new user + auto-login        |
| GET    | `/logout`          |  ✓   | Logout current user                 |
| GET    | `/admin/post/`     |  ✓   | Render create post form             |
| POST   | `/admin/post/`     |  ✓   | Create post (assign to current user)|

### Code Style
All code and comments are in English.
