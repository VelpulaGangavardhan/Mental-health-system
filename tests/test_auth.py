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
    """Test user registration and login flow"""
    rv = client.post('/register', data={'username': 'testuser', 'password': 'test123', 'confirm_password': 'test123'})
    assert rv.status_code == 302  # Redirect to login
    
    rv = client.post('/login', data={'username': 'testuser', 'password': 'test123'}, follow_redirects=True)
    assert b'Logged in successfully' in rv.data
    
    rv = client.get('/dashboard')
    assert rv.status_code == 200


def test_register_with_email(client):
    """Test user registration with email"""
    rv = client.post('/register', data={
        'username': 'emailuser',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    assert rv.status_code == 302  # Redirect to login
    
    # Test login with email
    rv = client.post('/login', data={'username': 'test@example.com', 'password': 'password123'}, follow_redirects=True)
    assert b'Logged in successfully' in rv.data


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    client.post('/register', data={'username': 'testuser', 'password': 'test123', 'confirm_password': 'test123'})
    
    rv = client.post('/login', data={'username': 'testuser', 'password': 'wrong'}, follow_redirects=True)
    assert b'Invalid username or password' in rv.data


def test_duplicate_username(client):
    """Test registration with duplicate username"""
    client.post('/register', data={'username': 'testuser', 'password': 'test123', 'confirm_password': 'test123'})
    
    rv = client.post('/register', data={'username': 'testuser', 'password': 'other', 'confirm_password': 'other'}, follow_redirects=True)
    assert b'Username already taken' in rv.data


def test_dashboard_after_login(client):
    """Test dashboard access after login"""
    # Register and login
    client.post('/register', data={'username': 'dashuser', 'password': 'pass123', 'confirm_password': 'pass123'})
    client.post('/login', data={'username': 'dashuser', 'password': 'pass123'}, follow_redirects=True)
    
    # Access dashboard
    rv = client.get('/dashboard')
    assert rv.status_code == 200
    assert b'Mental Health' in rv.data or b'dashboard' in rv.data.lower()


def test_dashboard_requires_login(client):
    """Test that dashboard requires authentication"""
    rv = client.get('/dashboard')
    assert rv.status_code == 302  # Redirect to login
    
    # Follow redirect
    rv = client.get('/dashboard', follow_redirects=True)
    assert b'login' in rv.data.lower()


def test_quick_screening_after_login(client):
    """Test quick screening after login"""
    # Register and login
    client.post('/register', data={'username': 'screenuser', 'password': 'pass123', 'confirm_password': 'pass123'})
    client.post('/login', data={'username': 'screenuser', 'password': 'pass123'})
    
    # Take screening
    rv = client.post('/screening', data={
        'q1': '2',
        'q2': '1',
        'q3': '0'
    }, follow_redirects=True)
    
    assert rv.status_code == 200
    assert b'score' in rv.data.lower() or b'result' in rv.data.lower()


def test_extended_screening_after_login(client):
    """Test extended screening after login"""
    # Register and login
    client.post('/register', data={'username': 'extuser', 'password': 'pass123', 'confirm_password': 'pass123'})
    client.post('/login', data={'username': 'extuser', 'password': 'pass123'})
    
    # Take extended screening
    rv = client.post('/extended-screening', data={
        'stress_q1': '2',
        'stress_q2': '1',
        'anxiety_q1': '1',
        'anxiety_q2': '0',
        'sleep_q1': '2',
        'sleep_q2': '2',
        'depression_q1': '1',
        'depression_q2': '0',
        'social_q1': '1',
        'social_q2': '1',
        'notes': 'Test notes'
    }, follow_redirects=True)
    
    assert rv.status_code == 200
    assert b'result' in rv.data.lower() or b'score' in rv.data.lower()


def test_profile_view_after_login(client):
    """Test profile view after login"""
    # Register and login
    client.post('/register', data={'username': 'profuser', 'password': 'pass123', 'confirm_password': 'pass123'})
    client.post('/login', data={'username': 'profuser', 'password': 'pass123'})
    
    # Access profile
    rv = client.get('/profile')
    assert rv.status_code == 200
    assert b'profuser' in rv.data or b'profile' in rv.data.lower()


def test_screening_history(client):
    """Test screening history page"""
    # Register, login, and take screening
    client.post('/register', data={'username': 'histuser', 'password': 'pass123', 'confirm_password': 'pass123'})
    client.post('/login', data={'username': 'histuser', 'password': 'pass123'})
    client.post('/screening', data={'q1': '2', 'q2': '1', 'q3': '0'})
    
    # View history
    rv = client.get('/history')
    assert rv.status_code == 200


def test_analytics_page(client):
    """Test analytics page"""
    # Register, login, and take screening
    client.post('/register', data={'username': 'analyticsuser', 'password': 'pass123', 'confirm_password': 'pass123'})
    client.post('/login', data={'username': 'analyticsuser', 'password': 'pass123'})
    client.post('/screening', data={'q1': '2', 'q2': '1', 'q3': '0'})
    
    # View analytics
    rv = client.get('/analytics')
    assert rv.status_code == 200


def test_logout(client):
    """Test logout functionality"""
    # Register and login
    client.post('/register', data={'username': 'logoutuser', 'password': 'pass123', 'confirm_password': 'pass123'})
    client.post('/login', data={'username': 'logoutuser', 'password': 'pass123'})
    
    # Logout
    rv = client.get('/logout', follow_redirects=True)
    assert b'logged out' in rv.data.lower()
    
    # Try accessing dashboard (should redirect)
    rv = client.get('/dashboard')
    assert rv.status_code == 302
