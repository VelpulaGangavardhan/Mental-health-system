import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Screening, CopingLog, Recommendation
from datetime import datetime

@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_user_password(session):
    """Test password hashing and verification"""
    u = User(username='alice')
    u.set_password('secret')
    session.add(u)
    session.commit()
    assert u.check_password('secret')
    assert not u.check_password('wrong')


def test_user_email_field(session):
    """Test user email field"""
    u = User(username='bob', email='bob@example.com')
    u.set_password('pw')
    session.add(u)
    session.commit()
    assert u.email == 'bob@example.com'
    assert u.username == 'bob'


def test_user_role_field(session):
    """Test user role (admin/user)"""
    u1 = User(username='user1', role='user')
    u1.set_password('pass123')
    u2 = User(username='admin1', role='admin')
    u2.set_password('pass123')
    session.add_all([u1, u2])
    session.commit()
    
    assert not u1.is_admin()
    assert u2.is_admin()


def test_user_timestamps(session):
    """Test user created_at and updated_at timestamps"""
    u = User(username='charlie')
    u.set_password('pw')
    session.add(u)
    session.commit()
    
    assert u.created_at is not None
    assert u.updated_at is not None
    assert isinstance(u.created_at, datetime)


def test_user_bio_field(session):
    """Test user bio field"""
    u = User(username='diana', bio='This is my bio')
    u.set_password('pw')
    session.add(u)
    session.commit()
    
    assert u.bio == 'This is my bio'


def test_screening_create(session):
    """Test basic screening creation"""
    u = User(username='bob')
    u.set_password('pw')
    session.add(u)
    session.commit()
    
    s = Screening(user_id=u.id, score=5, level='Moderate')
    session.add(s)
    session.commit()
    assert session.query(Screening).filter_by(user_id=u.id).count() == 1
    assert session.query(Screening).filter_by(user_id=u.id).first().level == 'Moderate'


def test_screening_component_scores(session):
    """Test screening with component scores"""
    u = User(username='eve')
    u.set_password('pw')
    session.add(u)
    session.commit()
    
    s = Screening(
        user_id=u.id,
        score=12,
        level='Moderate',
        stress_score=2,
        anxiety_score=3,
        sleep_score=2,
        depression_score=2,
        social_score=3
    )
    session.add(s)
    session.commit()
    
    screening = session.query(Screening).filter_by(user_id=u.id).first()
    assert screening.stress_score == 2
    assert screening.anxiety_score == 3
    assert screening.sleep_score == 2
    assert screening.depression_score == 2
    assert screening.social_score == 3
    assert screening.score == 12


def test_screening_notes(session):
    """Test screening notes field"""
    u = User(username='frank')
    u.set_password('pw')
    session.add(u)
    session.commit()
    
    s = Screening(user_id=u.id, score=10, level='Moderate', notes='Had a stressful day')
    session.add(s)
    session.commit()
    
    screening = session.query(Screening).filter_by(user_id=u.id).first()
    assert screening.notes == 'Had a stressful day'


def test_screening_timestamps(session):
    """Test screening created_at timestamp"""
    u = User(username='grace')
    u.set_password('pw')
    session.add(u)
    session.commit()
    
    s = Screening(user_id=u.id, score=5, level='Low')
    session.add(s)
    session.commit()
    
    screening = session.query(Screening).filter_by(user_id=u.id).first()
    assert screening.created_at is not None
    assert isinstance(screening.created_at, datetime)


def test_coping_log_create(session):
    """Test coping log creation"""
    u = User(username='henry')
    u.set_password('pw')
    session.add(u)
    session.commit()
    
    log = CopingLog(
        user_id=u.id,
        strategy='Deep breathing',
        description='Practiced 5 minutes of box breathing',
        effectiveness=4
    )
    session.add(log)
    session.commit()
    
    coping = session.query(CopingLog).filter_by(user_id=u.id).first()
    assert coping.strategy == 'Deep breathing'
    assert coping.effectiveness == 4


def test_coping_log_timestamps(session):
    """Test coping log timestamp"""
    u = User(username='isabella')
    u.set_password('pw')
    session.add(u)
    session.commit()
    
    log = CopingLog(user_id=u.id, strategy='Meditation')
    session.add(log)
    session.commit()
    
    coping = session.query(CopingLog).filter_by(user_id=u.id).first()
    assert coping.created_at is not None


def test_recommendation_create(session):
    """Test recommendation creation"""
    u = User(username='jack')
    u.set_password('pw')
    session.add(u)
    session.commit()
    
    s = Screening(user_id=u.id, score=15, level='High')
    session.add(s)
    session.commit()
    
    rec = Recommendation(
        screening_id=s.id,
        category='professional',
        title='Seek Professional Help',
        description='Consider talking to a therapist'
    )
    session.add(rec)
    session.commit()
    
    recommendation = session.query(Recommendation).filter_by(screening_id=s.id).first()
    assert recommendation.title == 'Seek Professional Help'
    assert recommendation.category == 'professional'


def test_screening_risk_levels(session):
    """Test different risk levels"""
    u = User(username='karen')
    u.set_password('pw')
    session.add(u)
    session.commit()
    
    low = Screening(user_id=u.id, score=3, level='Low')
    moderate = Screening(user_id=u.id, score=8, level='Moderate')
    high = Screening(user_id=u.id, score=18, level='High')
    
    session.add_all([low, moderate, high])
    session.commit()
    
    assert session.query(Screening).filter_by(level='Low').count() == 1
    assert session.query(Screening).filter_by(level='Moderate').count() == 1
    assert session.query(Screening).filter_by(level='High').count() == 1


def test_user_screenings_relationship(session):
    """Test user and screenings relationship"""
    u = User(username='lisa')
    u.set_password('pw')
    session.add(u)
    session.commit()
    
    for i in range(3):
        s = Screening(user_id=u.id, score=5+i, level='Low')
        session.add(s)
    session.commit()
    
    user = session.query(User).filter_by(username='lisa').first()
    assert len(user.screenings) == 3


def test_user_coping_logs_relationship(session):
    """Test user and coping logs relationship"""
    u = User(username='mike')
    u.set_password('pw')
    session.add(u)
    session.commit()
    
    for i in range(2):
        log = CopingLog(user_id=u.id, strategy=f'Strategy {i}')
        session.add(log)
    session.commit()
    
    user = session.query(User).filter_by(username='mike').first()
    assert len(user.coping_logs) == 2


def test_screening_recommendations_relationship(session):
    """Test screening and recommendations relationship"""
    u = User(username='nancy')
    u.set_password('pw')
    session.add(u)
    session.commit()
    
    s = Screening(user_id=u.id, score=15, level='High')
    session.add(s)
    session.commit()
    
    for i in range(3):
        rec = Recommendation(
            screening_id=s.id,
            category='coping',
            title=f'Recommendation {i}',
            description='Test'
        )
        session.add(rec)
    session.commit()
    
    screening = session.query(Screening).filter_by(user_id=u.id).first()
    assert len(screening.recommendations) == 3


def test_cascade_delete_screenings(session):
    """Test that deleting user cascades delete to screenings"""
    u = User(username='oscar')
    u.set_password('pw')
    session.add(u)
    session.commit()
    
    s = Screening(user_id=u.id, score=5, level='Low')
    session.add(s)
    session.commit()
    
    # Delete user
    session.delete(u)
    session.commit()
    
    # Screening should be deleted too
    assert session.query(Screening).filter_by(user_id=u.id).count() == 0


def test_unique_username_constraint(session):
    """Test username uniqueness"""
    u1 = User(username='paul')
    u1.set_password('pw')
    session.add(u1)
    session.commit()
    
    u2 = User(username='paul')
    u2.set_password('pw')
    session.add(u2)
    
    with pytest.raises(Exception):  # Should raise IntegrityError
        session.commit()