#!/usr/bin/env python
"""Initialize the database with the correct schema."""

from models import Base, engine, SessionLocal, User
from datetime import datetime
import os

# Drop all tables if they exist
Base.metadata.drop_all(bind=engine)

# Create all tables fresh
Base.metadata.create_all(bind=engine)

# Create a test admin user
session = SessionLocal()
try:
    admin = User(
        username='admin',
        email='admin@example.com',
        role='admin'
    )
    admin.set_password('admin123')
    session.add(admin)
    session.commit()
    print("✓ Admin user created (admin/admin123)")
    print("✓ Database initialized successfully!")
finally:
    session.close()

