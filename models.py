from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime, Text, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
engine = create_engine(DATABASE_URL, echo=False, future=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default='user', nullable=False)  # 'user' or 'admin'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    bio = Column(Text, nullable=True)
    preferences = Column(Text, nullable=True)  # JSON string for user preferences

    screenings = relationship('Screening', back_populates='user', cascade='all, delete-orphan')
    coping_logs = relationship('CopingLog', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f"<User {self.username}>"

class Screening(Base):
    __tablename__ = 'screenings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    score = Column(Integer, nullable=False)
    level = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)
    # Extended assessment fields
    stress_score = Column(Integer, nullable=True)
    anxiety_score = Column(Integer, nullable=True)
    sleep_score = Column(Integer, nullable=True)
    depression_score = Column(Integer, nullable=True)
    social_score = Column(Integer, nullable=True)

    user = relationship('User', back_populates='screenings')
    recommendations = relationship('Recommendation', back_populates='screening', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Screening {self.score} - {self.level}>"

class CopingLog(Base):
    __tablename__ = 'coping_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    strategy = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    effectiveness = Column(Integer, nullable=True)  # 1-5 rating
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='coping_logs')

    def __repr__(self):
        return f"<CopingLog {self.strategy}>"

class Recommendation(Base):
    __tablename__ = 'recommendations'

    id = Column(Integer, primary_key=True)
    screening_id = Column(Integer, ForeignKey('screenings.id'), nullable=False)
    category = Column(String(100), nullable=False)  # 'coping', 'resource', 'professional'
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    url = Column(String(500), nullable=True)

    screening = relationship('Screening', back_populates='recommendations')

    def __repr__(self):
        return f"<Recommendation {self.title}>"

def init_db():
    Base.metadata.create_all(engine)

# Backwards-compatible alias used by older code/tests
def create_tables():
    init_db()

