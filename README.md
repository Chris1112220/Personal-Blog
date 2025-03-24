# Personal Blog Backend API (Flask + PostgreSQL)

## Features
- User registration and login with JWT
- Authenticated blog post creation and retrieval
- PostgreSQL + SQLAlchemy for data persistence
- Token-protected routes

## Setup
```bash
git clone https://github.com/Chris1112220/Personal-Blog.git
cd Personal-Blog
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
set FLASK_APP=run.py
flask run