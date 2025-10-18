from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
import wtforms.fields #Imported here so that I can call input fields dynamically from csv e.g. DecimalField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
#from app.models import User
import pandas as pd


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In') # 'Log In' is used as an identifier in routes!


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up') # 'Sign Up' is used as an identifier in routes!


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


def create_investment_parameters_form(groups):
    def min_max_validator(max, min = 0):
        return NumberRange(min = min, max = max, 
            message = 'Please enter a number greater than {} and less than {}.'.format(min, max))

    class InvestmentParametersForm(FlaskForm):

        # Read in form field details and create fields
        df = pd.read_csv('form_fields.csv') 
        df = df[df['group'].isin(groups)]
        df = df.drop_duplicates(subset = ['name'], keep = 'last') # Override base fields if needed
        for i, row in df.iterrows():
            locals()[row['name']] = getattr(wtforms.fields, row['type'])(row['label'], default = row['default'], 
                description = row['description'],
                validators = [min_max_validator(max = row['max'], min = row['min'])])

        submit = SubmitField('Calculate')

    setattr(InvestmentParametersForm, 'groups', groups)
    return InvestmentParametersForm()