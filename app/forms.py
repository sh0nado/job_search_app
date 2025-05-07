from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

# Example LoginForm (to be expanded later)
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class UserProfileForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Profile')

    def __init__(self, original_email, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')

class SkillsSelectionForm(FlaskForm):
    skills = SelectMultipleField('Skills', coerce=int)
    submit = SubmitField('Save Skills') 