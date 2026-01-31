from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length, Email

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[DataRequired(), Length(min=3, max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ScreeningForm(FlaskForm):
    q1 = RadioField('I feel stressed frequently', choices=[('2','Often'),('1','Sometimes'),('0','Never')], validators=[DataRequired()])
    q2 = RadioField('I feel anxious or worried', choices=[('2','Often'),('1','Sometimes'),('0','Never')], validators=[DataRequired()])
    q3 = RadioField('I have trouble sleeping', choices=[('2','Often'),('1','Sometimes'),('0','Never')], validators=[DataRequired()])
    submit = SubmitField('Submit')