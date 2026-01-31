# Mental Health Platform (Enhanced)

This project is a simple Flask app for mental-health screening, now upgraded to include:

- SQLAlchemy ORM + Flask-Migrate
- Flask-Login authentication
- Flask-WTF forms (CSRF protection)
- Bootstrap-based responsive templates
- Unit tests with pytest
- Dockerfile + docker-compose for local dev

Quick start
1. Create and activate virtualenv (optional but recommended):
   - `python -m venv .venv` (Windows PowerShell: `.\.venv\Scripts\Activate.ps1`)
2. Install dependencies: `pip install -r requirements.txt`
3. Seed demo data: `python seed.py` (creates `demo / demo123`)
4. Start app locally: `python app.py` (visit `http://127.0.0.1:5000`)

Migrations
- To use migrations (recommended):
  - `flask db init`
  - `flask db migrate -m "Initial"`
  - `flask db upgrade`

Run tests
- `pytest -q`

Docker
- `docker-compose up --build`

If you'd like, I can now:
- Add more fields to the `Screening` model and make screenings configurable
- Add CI to run tests and linting automatically
- Convert to a package layout (app factory) for better testability

Which would you like next?