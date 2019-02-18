# encoding: utf-8
# create forms here

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Optional, Email, Length
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms import ValidationError
from app.models import User


class signupForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email(message='Invalid email add')])
    username = StringField(validators=[DataRequired(), Length(3, 15, message='Username length between 3-15')])
    password = PasswordField(validators=[DataRequired(), Length(6, 15, message='Password length between 6-15')])
    confirm = PasswordField(validators=[DataRequired(), EqualTo('password', message='Password not matches')])
    submit = SubmitField()

    # two customized functions for validating usename and email
    # must be started with 'validate_'
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(message='Username already taken!')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered!')


class loginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email(message='Invalid email add')])
    password = PasswordField(validators=[DataRequired(), Length(6, 15, message='Password length between 6-15')])
    submit = SubmitField()
