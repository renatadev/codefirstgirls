from flask_wtf import FlaskForm  #import our forms without using html but using python classes and a flask extension
from wtforms import StringField, PasswordField, SubmitField, BooleanField #for fields that are imported from wtf package
from wtforms.validators import DataRequired, Length, Email, EqualTo #non empty validator, etc


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)]) #valitors so we get real username, long enough, non-empty etc
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
