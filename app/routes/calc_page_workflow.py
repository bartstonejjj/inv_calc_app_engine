from app import app
from app.forms import create_investment_parameters_form
from app.routes.lib import add_calc_record, load_global_vars
from app.routes.guest_user_manager import guest_login_allowed, is_guest_user
from flask import g, render_template, session, redirect, url_for
from flask_login import logout_user
import requests
import simplejson as json

def invalid_data_submitted_check(form, calc_name, ip):
    with app.app_context():
        if form.is_submitted() and not form.validate(): # Invalid data entered
            add_calc_record(calc_name = calc_name, form = form, ip = ip, valid = False)
            return True
        return False

def render_calc_page(rebuilder, form, calc_name, ip, html_file, cache_name,
    falsk_g, global_vars):

    falsk_g = falsk_g.__dict__

    with app.app_context():

        # Update current app_context with previous flask.g
        for k,v in falsk_g.items():
            setattr(g, k, v)

        # Global variables to display content for each model
        for k,v in global_vars.items():
            setattr(g, k, v)

        # ------------- temporarily turned off db
        if is_guest_user(app) and not guest_login_allowed(ip):
            logout_user()
            return redirect(url_for('login_page'))
        # ----------------------------------------

        invalid_data_submitted = invalid_data_submitted_check(form, calc_name, ip)

        if form.validate_on_submit():
            add_calc_record(calc_name = calc_name, form = form, ip = ip)

            # Calculate investment and return variables
            payload = {"form_data": form.data}
            resp = requests.post(
                "http://127.0.0.1:5001/calc_fund",
                data=json.dumps(payload, use_decimal=True),
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            print(resp)
            res = rebuilder(resp, form)
            print(res)

            page = render_template(html_file, **res.html_vars)
            app.cache.set(cache_name, page)
            return page

        page = app.cache.get(cache_name)
        if page and not invalid_data_submitted:
            return page

        # else:
        return render_template(html_file, title='Home', form=form, data = None)


