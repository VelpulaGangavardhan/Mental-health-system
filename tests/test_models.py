import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Screening

@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_user_password(session):
    u = User(username='alice')
    u.set_password('secret')
    session.add(u)
    session.commit()
    assert u.check_password('secret')
    assert not u.check_password('wrong')


def test_screening_create(session):
    u = User(username='bob')
    u.set_password('pw')
    session.add(u)
    session.commit()
    s = Screening(user_id=u.id, score=5, level='Moderate')
    session.add(s)
    session.commit()
    assert session.query(Screening).filter_by(user_id=u.id).count() == 1
    assert session.query(Screening).filter_by(user_id=u.id).first().level == 'Moderate'