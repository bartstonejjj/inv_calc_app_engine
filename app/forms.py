from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
import wtforms.fields #Imported here so that I can call input fields dynamically from csv e.g. DecimalField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
#from app.models import User
import csv


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


def min_max_validator(max, min=0):
    return NumberRange(min=min, max=max,
                       message='Please enter a number greater than {} and less than {}.'.format(min, max))


def create_investment_parameters_form(groups):
    class InvestmentParametersForm(FlaskForm):
        rows = []

        # 1️⃣ Read CSV manually
        with open('form_fields.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('group') in groups:
                    rows.append(row)

        # 2️⃣ Remove duplicates by 'name', keeping the last one
        unique_rows = {}
        for row in rows:
            unique_rows[row['name']] = row  # later rows overwrite earlier ones
        rows = list(unique_rows.values())
        print(row)

        # 3️⃣ Dynamically create WTForm fields
        for row in rows:
            locals()[row['name']] = getattr(wtforms.fields, row['type'])(row['label'], default=row['default'],
                description=row['description'], validators=[min_max_validator(max=float(row['max']), min=float(row['min']))])

        submit = SubmitField('Calculate')

    setattr(InvestmentParametersForm, 'groups', groups)
    return InvestmentParametersForm()