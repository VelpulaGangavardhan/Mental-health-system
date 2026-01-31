from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions (no app bound yet)
db = SQLAlchemy()
migrate = Migrate()