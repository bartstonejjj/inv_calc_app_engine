# For Flask
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse
from app import app, db, firebase
from app.forms import LoginForm, RegistrationForm
from app.models import User
from app.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email
from flask import g, request
from app.routes.lib import add_login_record, redirect_to_next_page, load_global_vars, get_client_ip
from app.routes.guest_user_manager import guest_login_allowed, time_since_last_login, calcs_count, calc_quota_exceeded
from requests.exceptions import HTTPError
from app.routes.firebase_lib import try_create_user, try_sign_in_user, try_get_user_by_email
from firebase_admin import auth

from app.routes.p2p import p2p_page
from app.routes.property import property_page
from app.routes.fund import fund_page
import datetime

# Map all http requests to https
# As per: https://flask.palletsprojects.com/en/master/security/#security-csp
# and: https://stackoverflow.com/questions/30717152/python-flask-how-to-set
# -response-header-for-all-responses?lq=1
@app.after_request
def apply_caching(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Investment Calculator')

def render_landing_page(login_form, register_form, login_error = False, login_error_message=False,
    signup_error = False, signup_error_message = False):
    return render_template('landing.html', title='Log In', 
        login_form=login_form, login_error=login_error, login_error_message=login_error_message, 
        register_form=register_form, signup_error=signup_error, signup_error_message=signup_error_message)

# Any user that doesn't pass test login_required gets redircted to route with function 'login'
@app.route('/', methods=['GET', 'POST'])
@app.route('/auto_login', methods=['GET', 'POST'])
def login():
    ip = get_client_ip(app)
    print('ip', ip)
    
    timeframe = datetime.timedelta(days = 1)
    calc_quota = 3
    print('calcs_count', calcs_count(ip, timeframe))
    print('calc_quota_exceeded', calc_quota_exceeded(ip, calc_quota, timeframe))
    print('guest_login_allowed', guest_login_allowed(ip, calc_quota, timeframe))
    print('current_user.is_authenticated', current_user.is_authenticated)

    if current_user.is_authenticated:
        return redirect_to_next_page(app)

    if guest_login_allowed(ip, calc_quota, timeframe):
        guest_user = User(user = {'localId':0})
        logged_in = login_user(guest_user, remember=False)
        add_login_record(user_id = 0, ip = ip)
        return redirect_to_next_page(app)

    else:
        return redirect(url_for('login_page'))
        

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    ip = request.remote_addr
    login_form = LoginForm()
    register_form = RegistrationForm()
    login_error = False
    login_submit = False
    register_submit = False
    signup_error = False

    if 'form' in request.__dict__:
        login_submit = True if request.form['submit'] == 'Log In' else False
        register_submit = True if request.form['submit'] == 'Sign Up' else False

    # Invalid Sign Up
    if register_form.is_submitted() and not register_form.validate() and register_submit:
        return render_landing_page(LoginForm(), register_form, signup_error = True)   

    # Try Sign Up
    if register_form.validate_on_submit() and register_submit:
        login_form = LoginForm() # Reset other form so it doesn't interfere

        user, error, error_message = try_create_user(
            email = register_form.email.data, 
            password = register_form.password.data)

        # Invalid Sign Up
        if error:
            return render_landing_page(login_form, register_form, 
                signup_error = error,
                signup_error_message = error_message)

        # Valid Sign Up
        else:
            flash('Congratulations, you are now a registered user!')
            login_user(User(user))
            return render_landing_page(login_form, register_form)
    
    # Invalid Log In
    if login_form.is_submitted() and not login_form.validate() and login_submit:
        return render_landing_page(login_form, RegistrationForm(), login_error = True)

    # Try Log In
    if login_form.validate_on_submit() and login_submit:
        register_form = RegistrationForm() # Reset other form so it doesn't interfere
        
        user, error, error_message = try_sign_in_user(
            email = register_form.email.data, 
            password = register_form.password.data)

        # Invalid Log In
        if user is None or error:
            return render_landing_page(login_form, register_form, 
                login_error = error,
                login_error_message = error_message)
        
        # Valid Log In
        else:
            login_user(User(user), remember=login_form.remember_me.data)
            add_login_record(user_id = user['localId'], ip = ip)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                return render_landing_page(login_form, register_form)
            return redirect(next_page)
    return render_landing_page(login_form, register_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page'))


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


@app.route('/blog', methods=['GET'])
def blog():
    return render_template('blog.html')

# TO DO - Try to add all these blogs these in more dynamically
@app.route('/blog/buy-vs-rent', methods=['GET'])
def buyvsrent():
    return render_template('content/blog/buy-vs-rent.html')


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = try_get_user_by_email(form.email.data)
        if user:
            send_password_reset_email(User(user))
        flash('Please check your email for instructions to reset your password.')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
        title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        print('reset_password', 'is_authenticated')
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    print('user', user)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        auth.update_user(user['localId'], password=form.password.data)
        flash('Your password has been reset!')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)