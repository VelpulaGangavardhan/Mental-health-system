from flask import Flask, render_template, redirect, flash, url_for, request, jsonify, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import User, Screening, CopingLog, Recommendation, SessionLocal, init_db
from forms import LoginForm, RegisterForm, ScreeningForm, ExtendedScreeningForm, ProfileForm, ChangePasswordForm, CopingLogForm
from datetime import datetime, timedelta
import os
import json
from functools import wraps
import csv
from io import StringIO, BytesIO

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
        user = session.query(User).filter(User.id == int(user_id)).first()
        return user
    except:
        return None
    finally:
        session.close()


@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# Helper function to get user ID safely
def get_user_id():
    """Get current user ID safely from Flask-Login"""
    try:
        return int(current_user.get_id())
    except:
        try:
            return int(current_user.id)
        except:
            return None

# Admin decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Helper function to get recommendations
def get_recommendations(score, level, screening_id):
    recommendations = []
    
    if level == 'High':
        recommendations = [
            {'category': 'professional', 'title': 'Consider Professional Help', 'description': 'Your assessment suggests you may benefit from speaking with a mental health professional.'},
            {'category': 'coping', 'title': 'Grounding Technique', 'description': 'Try the 5-4-3-2-1 technique: Notice 5 things you see, 4 you touch, 3 you hear, 2 you smell, 1 you taste.'},
            {'category': 'resource', 'title': 'Mental Health Hotline', 'description': 'Call 988 (Suicide & Crisis Lifeline) for immediate support anytime.'},
        ]
    elif level == 'Moderate':
        recommendations = [
            {'category': 'coping', 'title': 'Deep Breathing Exercise', 'description': 'Try Box Breathing: Breathe in for 4 counts, hold for 4, out for 4, hold for 4.'},
            {'category': 'coping', 'title': 'Physical Activity', 'description': 'Regular exercise can improve mental health. Aim for 30 minutes daily.'},
            {'category': 'resource', 'title': 'Meditation Apps', 'description': 'Try apps like Headspace or Calm for guided meditation and mindfulness.'},
        ]
    else:  # Low
        recommendations = [
            {'category': 'coping', 'title': 'Maintain Healthy Habits', 'description': 'Keep up with exercise, sleep, and social connections.'},
            {'category': 'resource', 'title': 'Wellness Tips', 'description': 'Continue with self-care practices and stress management techniques.'},
        ]
    
    session = SessionLocal()
    try:
        for rec in recommendations:
            r = Recommendation(screening_id=screening_id, **rec)
            session.add(r)
        session.commit()
    finally:
        session.close()
    
    return recommendations


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
        email = form.email.data
        password = form.password.data

        session = SessionLocal()
        try:
            if session.query(User).filter_by(username=username).first():
                flash('Username already taken.', 'warning')
                return redirect(url_for('register'))
            
            if email and session.query(User).filter_by(email=email).first():
                flash('Email already registered.', 'warning')
                return redirect(url_for('register'))

            user = User(username=username, email=email)
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
            if not user:
                user = session.query(User).filter_by(email=username).first()
            
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
    if not current_user.is_authenticated:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    
    session = SessionLocal()
    try:
        # Get user ID safely
        try:
            user_id = int(current_user.get_id())
        except:
            user_id = int(current_user.id)
        
        # Get recent screenings
        screenings = session.query(Screening).filter_by(user_id=user_id).order_by(Screening.created_at.desc()).limit(10).all()
        data = [(s.created_at.strftime('%Y-%m-%d'), s.score, s.level) for s in screenings]
        
        # Get statistics
        total_screenings = session.query(Screening).filter_by(user_id=user_id).count()
        avg_score = session.query(func.avg(Screening.score)).filter_by(user_id=user_id).scalar() or 0
        
        return render_template('dashboard.html', data=data, total_screenings=total_screenings, avg_score=round(avg_score, 2))
    except Exception as e:
        print(f'Dashboard error: {str(e)}')
        flash('Error loading dashboard. Please try again.', 'danger')
        return redirect(url_for('index'))
    finally:
        session.close()


# SCREENING
@app.route('/screening', methods=['GET', 'POST'])
@login_required
def screening():
    form = ScreeningForm()
    if form.validate_on_submit():
        answers = [int(getattr(form, f'q{i}').data) for i in range(1, 11)]
        score = sum(answers)
        if score <= 8:
            level = 'Low'
        elif score <= 15:
            level = 'Moderate'
        else:
            level = 'High'

        session = SessionLocal()
        try:
            user_id = get_user_id()
            if not user_id:
                flash('User session expired. Please log in again.', 'warning')
                return redirect(url_for('login'))
            s = Screening(user_id=user_id, score=score, level=level)
            session.add(s)
            session.commit()
            
            # Generate recommendations
            recommendations = get_recommendations(score, level, s.id)
            
            return render_template('result.html', score=score, level=level, recommendations=recommendations)
        finally:
            session.close()
    return render_template('screening.html', form=form)

# EXTENDED SCREENING
@app.route('/extended-screening', methods=['GET', 'POST'])
@login_required
def extended_screening():
    form = ExtendedScreeningForm()
    if form.validate_on_submit():
        session = SessionLocal()
        try:
            # Calculate component scores
            stress_score = int(form.stress_q1.data) + int(form.stress_q2.data)
            anxiety_score = int(form.anxiety_q1.data) + int(form.anxiety_q2.data)
            sleep_score = int(form.sleep_q1.data) + int(form.sleep_q2.data)
            depression_score = int(form.depression_q1.data) + int(form.depression_q2.data)
            social_score = int(form.social_q1.data) + int(form.social_q2.data)
            
            total_score = stress_score + anxiety_score + sleep_score + depression_score + social_score
            
            if total_score <= 15:
                level = 'Low'
            elif total_score <= 30:
                level = 'Moderate'
            else:
                level = 'High'
            
            s = Screening(
                user_id=get_user_id() or current_user.id,
                score=total_score,
                level=level,
                stress_score=stress_score,
                anxiety_score=anxiety_score,
                sleep_score=sleep_score,
                depression_score=depression_score,
                social_score=social_score,
                notes=form.notes.data
            )
            session.add(s)
            session.commit()
            
            # Generate recommendations
            recommendations = get_recommendations(total_score, level, s.id)
            
            return render_template('extended_result.html', 
                                 total_score=total_score, 
                                 level=level,
                                 stress_score=stress_score,
                                 anxiety_score=anxiety_score,
                                 sleep_score=sleep_score,
                                 depression_score=depression_score,
                                 social_score=social_score,
                                 recommendations=recommendations)
        finally:
            session.close()
    
    return render_template('extended_screening.html', form=form)

# USER PROFILE
@app.route('/profile')
@login_required
def profile():
    session = SessionLocal()
    try:
        user_id = get_user_id()
        if not user_id:
            flash('User session expired. Please log in again.', 'warning')
            return redirect(url_for('login'))
        user = session.query(User).get(user_id)
        screening_count = session.query(Screening).filter_by(user_id=user_id).count()
        return render_template('profile.html', user=user, screening_count=screening_count)
    finally:
        session.close()

# EDIT PROFILE
@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    session = SessionLocal()
    try:
        user_id = get_user_id()
        if not user_id:
            flash('User session expired. Please log in again.', 'warning')
            return redirect(url_for('login'))
        user = session.query(User).get(user_id)
        
        if form.validate_on_submit():
            if form.username.data != user.username:
                if session.query(User).filter_by(username=form.username.data).first():
                    flash('Username already taken.', 'warning')
                    return redirect(url_for('edit_profile'))
            
            user.username = form.username.data
            user.email = form.email.data
            user.bio = form.bio.data
            user.updated_at = datetime.utcnow()
            session.commit()
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
        elif request.method == 'GET':
            form.username.data = user.username
            form.email.data = user.email
            form.bio.data = user.bio
        
        return render_template('edit_profile.html', form=form)
    finally:
        session.close()

# CHANGE PASSWORD
@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    session = SessionLocal()
    try:
        user_id = get_user_id()
        if not user_id:
            flash('User session expired. Please log in again.', 'warning')
            return redirect(url_for('login'))
        user = session.query(User).get(user_id)
        
        if form.validate_on_submit():
            if not user.check_password(form.current_password.data):
                flash('Current password is incorrect.', 'danger')
                return redirect(url_for('change_password'))
            
            user.set_password(form.new_password.data)
            user.updated_at = datetime.utcnow()
            session.commit()
            
            flash('Password changed successfully!', 'success')
            return redirect(url_for('profile'))
        
        return render_template('change_password.html', form=form)
    finally:
        session.close()

# SCREENING HISTORY
@app.route('/history')
@login_required
def screening_history():
    session = SessionLocal()
    try:
        user_id = get_user_id()
        if not user_id:
            flash('User session expired. Please log in again.', 'warning')
            return redirect(url_for('login'))
        screenings = session.query(Screening).filter_by(user_id=user_id).order_by(Screening.created_at.desc()).all()
        
        # Prepare data for chart
        chart_data = [{
            'date': s.created_at.strftime('%Y-%m-%d'),
            'score': s.score,
            'level': s.level
        } for s in screenings]
        
        return render_template('screening_history.html', screenings=screenings, chart_data=json.dumps(chart_data))
    finally:
        session.close()

# ANALYTICS
@app.route('/analytics')
@login_required
def analytics():
    session = SessionLocal()
    try:
        user_id = get_user_id()
        if not user_id:
            flash('User session expired. Please log in again.', 'warning')
            return redirect(url_for('login'))
        screenings = session.query(Screening).filter_by(user_id=user_id).order_by(Screening.created_at.desc()).all()
        
        if not screenings:
            flash('No screening data available.', 'info')
            return render_template('analytics.html', stats={})
        
        scores = [s.score for s in screenings]
        levels = [s.level for s in screenings]
        
        stats = {
            'total': len(screenings),
            'avg_score': round(sum(scores) / len(scores), 2),
            'min_score': min(scores),
            'max_score': max(scores),
            'last_screening': screenings[0].created_at.strftime('%Y-%m-%d'),
            'trend': 'Improving' if screenings[0].score < screenings[-1].score else 'Worsening' if screenings[0].score > screenings[-1].score else 'Stable',
            'level_distribution': {
                'Low': levels.count('Low'),
                'Moderate': levels.count('Moderate'),
                'High': levels.count('High')
            }
        }
        
        return render_template('analytics.html', stats=stats, screenings=screenings)
    finally:
        session.close()

# COPING STRATEGIES
@app.route('/coping-strategies')
@login_required
def coping_strategies():
    session = SessionLocal()
    try:
        user_id = get_user_id()
        if not user_id:
            flash('User session expired. Please log in again.', 'warning')
            return redirect(url_for('login'))
        strategies = session.query(CopingLog).filter_by(user_id=user_id).order_by(CopingLog.created_at.desc()).all()
        return render_template('coping_strategies.html', strategies=strategies)
    finally:
        session.close()

# LOG COPING STRATEGY
@app.route('/log-strategy', methods=['GET', 'POST'])
@login_required
def log_strategy():
    form = CopingLogForm()
    session = SessionLocal()
    try:
        if form.validate_on_submit():
            user_id = get_user_id()
            if not user_id:
                flash('User session expired. Please log in again.', 'warning')
                return redirect(url_for('login'))
            log = CopingLog(
                user_id=user_id,
                strategy=form.strategy.data,
                description=form.description.data,
                effectiveness=int(form.effectiveness.data) if form.effectiveness.data else None
            )
            session.add(log)
            session.commit()
            flash('Strategy logged successfully!', 'success')
            return redirect(url_for('coping_strategies'))
        
        return render_template('log_strategy.html', form=form)
    finally:
        session.close()

# EXPORT DATA
@app.route('/export-data')
@login_required
def export_data():
    session = SessionLocal()
    try:
        user_id = get_user_id()
        if not user_id:
            flash('User session expired. Please log in again.', 'warning')
            return redirect(url_for('login'))
        screenings = session.query(Screening).filter_by(user_id=user_id).order_by(Screening.created_at).all()
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Date', 'Score', 'Level', 'Stress', 'Anxiety', 'Sleep', 'Depression', 'Social', 'Notes'])
        
        for s in screenings:
            writer.writerow([
                s.created_at.strftime('%Y-%m-%d %H:%M'),
                s.score,
                s.level,
                s.stress_score or '',
                s.anxiety_score or '',
                s.sleep_score or '',
                s.depression_score or '',
                s.social_score or '',
                s.notes or ''
            ])
        
        output.seek(0)
        # send_file requires a binary file-like object; encode CSV to bytes
        csv_bytes = output.getvalue().encode('utf-8')
        bytes_io = BytesIO(csv_bytes)
        bytes_io.seek(0)
        return send_file(
            bytes_io,
            mimetype='text/csv; charset=utf-8',
            as_attachment=True,
            download_name=f'screening_data_{datetime.now().strftime("%Y%m%d")}.csv'
        )
    finally:
        session.close()

# ADMIN DASHBOARD
@app.route('/admin')
@admin_required
def admin_dashboard():
    session = SessionLocal()
    try:
        total_users = session.query(User).count()
        total_screenings = session.query(Screening).count()
        users = session.query(User).all()
        
        return render_template('admin_dashboard.html', 
                             total_users=total_users,
                             total_screenings=total_screenings,
                             users=users)
    finally:
        session.close()

# ADMIN USER MANAGEMENT
@app.route('/admin/users/<int:user_id>/toggle-admin', methods=['POST'])
@admin_required
def toggle_admin(user_id):
    session = SessionLocal()
    try:
        user = session.query(User).get(user_id)
        if user:
            user.role = 'admin' if user.role != 'admin' else 'user'
            session.commit()
            flash(f'User {user.username} role updated.', 'success')
        return redirect(url_for('admin_dashboard'))
    finally:
        session.close()

# ADMIN DELETE USER
@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    if user_id == current_user.id:
        flash('Cannot delete your own account.', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    session = SessionLocal()
    try:
        user = session.query(User).get(user_id)
        if user:
            session.delete(user)
            session.commit()
            flash(f'User {user.username} deleted.', 'success')
        return redirect(url_for('admin_dashboard'))
    finally:
        session.close()

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
