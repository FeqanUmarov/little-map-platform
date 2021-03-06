from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from map.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Istifadeci Adi',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Parol', validators=[DataRequired()])
    confirm_password = PasswordField('Tekrar Parol',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Qeydiyyat')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Bu istifadeci adi mövcuddur xahis edirik başqa email daxil edin!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Bu email mövcuddur xahis edirik başqa ad daxil edin!')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Parol', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Giriş et')