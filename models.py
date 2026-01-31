from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
engine = create_engine(DATABASE_URL, echo=False, future=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    screenings = relationship('Screening', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def __repr__(self):
        return f"<User {self.username}>"

class Screening(Base):
    __tablename__ = 'screenings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    score = Column(Integer, nullable=False)
    level = Column(String(50), nullable=False)

    user = relationship('User', back_populates='screenings')

    def __repr__(self):
        return f"<Screening {self.score} - {self.level}>"

def init_db():
    Base.metadata.create_all(engine)

# Backwards-compatible alias used by older code/tests
def create_tables():
    init_db()

