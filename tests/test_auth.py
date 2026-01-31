import pytest
from app import app
import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def client():
    # Use an in-memory DB for tests and inject into models.SessionLocal
    engine = create_engine('sqlite:///:memory:')
    models.Base.metadata.create_all(engine)
    models.SessionLocal = sessionmaker(bind=engine)

    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        yield client


def test_register_and_login(client):
    rv = client.post('/register', data={'username': 'testuser', 'password': 'test123'}, follow_redirects=True)
    assert b'Account created' in rv.data
    rv = client.post('/login', data={'username': 'testuser', 'password': 'test123'}, follow_redirects=True)
    assert b'Logged in successfully' in rv.data
    rv = client.get('/dashboard')
    assert rv.status_code == 200
