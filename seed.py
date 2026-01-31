from models import User, Screening, SessionLocal, init_db

if __name__ == '__main__':
    init_db()
    session = SessionLocal()
    try:
        demo = session.query(User).filter_by(username='demo').first()
        if not demo:
            demo = User(username='demo')
            demo.set_password('demo123')
            session.add(demo)
            session.commit()
            print('Created demo user: demo / demo123')
        else:
            print('Demo user already exists')

        # Add sample screening results (skip duplicates)
        existing = session.query(Screening).filter_by(user_id=demo.id).count()
        if existing == 0:
            s1 = Screening(user_id=demo.id, score=6, level='Moderate')
            s2 = Screening(user_id=demo.id, score=3, level='Low')
            session.add_all([s1, s2])
            session.commit()
            print('Seeded screening sample data')
        else:
            print('Screening samples already present')
    finally:
        session.close()