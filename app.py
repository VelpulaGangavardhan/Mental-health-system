from flask import Flask, render_template, redirect, flash, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.orm import Session
from models import User, Screening, SessionLocal, init_db
from forms import LoginForm, RegisterForm, ScreeningForm
import os

# Basic app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mindcare_secret')

# Ensure tables exist (Flask 3 + pytest safe)
from models import create_tables
create_tables()

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = SessionLocal()
    try:
        user = session.get(User, int(user_id))
        return user
    finally:
        session.close()


@app.context_processor
def inject_user():
    return dict(current_user=current_user)





@app.route('/')
def index():
    return render_template('index.html')


@app.route('/awareness')
def awareness():
    return render_template('awareness.html')


@app.route('/support')
def support():
    return render_template('support.html')


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        session = SessionLocal()
        try:
            if session.query(User).filter_by(username=username).first():
                flash('Username already taken.', 'warning')
                return redirect(url_for('register'))

            user = User(username=username)
            user.set_password(password)
            session.add(user)
            session.commit()
            flash('Account created. Please log in.', 'success')
            return redirect(url_for('login'))
        finally:
            session.close()

    return render_template('register.html', form=form)

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        session = SessionLocal()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Logged in successfully.', 'success')
                next_page = url_for('dashboard')
                return redirect(next_page)
            flash('Invalid username or password.', 'danger')
        finally:
            session.close()
    return render_template('login.html', form=form)

# DASHBOARD
@app.route('/dashboard')
@login_required
def dashboard():
    session = SessionLocal()
    try:
        data = [(s.score, s.level) for s in session.query(Screening).filter_by(user_id=current_user.id).order_by(Screening.id.desc()).all()]
        return render_template('dashboard.html', data=data)
    finally:
        session.close()


# SCREENING
@app.route('/screening', methods=['GET', 'POST'])
@login_required
def screening():
    form = ScreeningForm()
    if form.validate_on_submit():
        answers = [int(getattr(form, f'q{i}').data) for i in range(1, 4)]
        score = sum(answers)
        if score <= 4:
            level = 'Low'
        elif score <= 8:
            level = 'Moderate'
        else:
            level = 'High'

        session = SessionLocal()
        try:
            s = Screening(user_id=current_user.id, score=score, level=level)
            session.add(s)
            session.commit()
            return render_template('result.html', score=score, level=level)
        finally:
            session.close()
    return render_template('screening.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
