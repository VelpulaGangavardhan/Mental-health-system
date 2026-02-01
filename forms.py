from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Optional, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=120)])
    email = StringField('Email', validators=[Email(), Optional()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[DataRequired(), Length(min=3, max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ScreeningForm(FlaskForm):
    q1 = RadioField('I feel stressed frequently', choices=[('2','Often'),('1','Sometimes'),('0','Never')], validators=[DataRequired()])
    q2 = RadioField('I feel anxious or worried', choices=[('2','Often'),('1','Sometimes'),('0','Never')], validators=[DataRequired()])
    q3 = RadioField('I have trouble sleeping', choices=[('2','Often'),('1','Sometimes'),('0','Never')], validators=[DataRequired()])
    q4 = RadioField('I feel sad or depressed', choices=[('2','Often'),('1','Sometimes'),('0','Never')], validators=[DataRequired()])
    q5 = RadioField('I have difficulty concentrating', choices=[('2','Often'),('1','Sometimes'),('0','Never')], validators=[DataRequired()])
    q6 = RadioField('I feel isolated or lonely', choices=[('2','Often'),('1','Sometimes'),('0','Never')], validators=[DataRequired()])
    q7 = RadioField('I have lost interest in activities I enjoy', choices=[('2','Often'),('1','Sometimes'),('0','Never')], validators=[DataRequired()])
    q8 = RadioField('I experience appetite changes', choices=[('2','Often'),('1','Sometimes'),('0','Never')], validators=[DataRequired()])
    q9 = RadioField('I feel overwhelmed by my responsibilities', choices=[('2','Often'),('1','Sometimes'),('0','Never')], validators=[DataRequired()])
    q10 = RadioField('I have thoughts of harming myself', choices=[('2','Often'),('1','Sometimes'),('0','Never')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class ExtendedScreeningForm(FlaskForm):
    # Stress Assessment
    stress_q1 = RadioField('How often do you feel stressed?', choices=[('2','Often'),('1','Sometimes'),('0','Never')], validators=[DataRequired()])
    stress_q2 = RadioField('How do you manage stress?', choices=[('0','Well'),('1','Somewhat'),('2','Poorly')], validators=[DataRequired()])
    
    # Anxiety Assessment
    anxiety_q1 = RadioField('How often do you experience anxiety?', choices=[('2','Often'),('1','Sometimes'),('0','Never')], validators=[DataRequired()])
    anxiety_q2 = RadioField('How much does anxiety affect your daily life?', choices=[('0','Minimal'),('1','Moderate'),('2','Significant')], validators=[DataRequired()])
    
    # Sleep Assessment
    sleep_q1 = RadioField('How many hours do you typically sleep?', choices=[('2','<6 hours'),('1','6-7 hours'),('0','8+ hours')], validators=[DataRequired()])
    sleep_q2 = RadioField('How is your sleep quality?', choices=[('2','Poor'),('1','Fair'),('0','Good')], validators=[DataRequired()])
    
    # Depression Assessment
    depression_q1 = RadioField('How often do you feel down or depressed?', choices=[('2','Often'),('1','Sometimes'),('0','Never')], validators=[DataRequired()])
    depression_q2 = RadioField('Do you enjoy activities you usually enjoy?', choices=[('0','Yes'),('1','Sometimes'),('2','No')], validators=[DataRequired()])
    
    # Social Assessment
    social_q1 = RadioField('How is your social connection with others?', choices=[('0','Strong'),('1','Moderate'),('2','Weak')], validators=[DataRequired()])
    social_q2 = RadioField('Do you have someone to talk to?', choices=[('0','Yes'),('1','Sometimes'),('2','No')], validators=[DataRequired()])
    
    notes = TextAreaField('Any additional notes?', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Complete Assessment')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=120)])
    email = StringField('Email', validators=[Email(), Optional()])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Update Profile')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

class CopingLogForm(FlaskForm):
    strategy = StringField('Coping Strategy', validators=[DataRequired(), Length(min=3, max=255)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    effectiveness = SelectField('Effectiveness (1-5)', choices=[(str(i), str(i)) for i in range(1, 6)], validators=[Optional()])
    submit = SubmitField('Log Strategy')