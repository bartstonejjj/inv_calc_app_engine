from app import app
from app.routes.lib import add_calc_record
from app.routes.guest_user_manager import guest_login_allowed, is_guest_user
from flask import g, render_template, redirect, url_for
from flask_login import logout_user
import requests
import simplejson as json
import ast
from app.routes.calc_lib import rebuild_CalcVars


def invalid_data_submitted_check(form, calc_name, ip):
    with app.app_context():
        if form.is_submitted() and not form.validate(): # Invalid data entered
            add_calc_record(calc_name = calc_name, form = form, ip = ip, valid = False)
            return True
        return False


def group_headers(flat_headers):
    grouped = []
    current_group = None
    current_items = []

    for g, s in flat_headers:
        # Handle standalone headers (no subgroup)
        if not g or not s:
            # flush any open group
            if current_items:
                grouped.append(current_items)
                current_items = []
            grouped.append([g or s])
            current_group = None
            continue

        # New group encountered
        if g != current_group:
            if current_items:
                grouped.append(current_items)
            current_group = g
            current_items = []

        current_items.append([g, s])

    # Add any remaining group
    if current_items:
        grouped.append(current_items)

    return grouped


# used for big_table rendering
def convert_dataframe_var(data):
    # Parse tuple-like keys into real tuples
    parsed = []
    for k, v in data.items():
        try:
            key = list(ast.literal_eval(k))
        except Exception:
            key = [k]
        parsed.append((key, v))

    # Build headers (list of lists) (get rid of empty column names to force merged cells)
    raw_headers = [key for key, _ in parsed]
    headers = group_headers(raw_headers)

    # Determine all row indices (whatever the inner dict keys are)
    all_indices = sorted({int(i) for _, vals in parsed for i in vals.keys()})

    # Build rows (list of lists)
    rows = []
    for i in all_indices:
        row = []
        for _, vals in parsed:
            row.append(vals.get(str(i)))
        rows.append(row)

    return {"headers": headers, "rows": rows}


def render_calc_page(cloud_run_route, form, calc_name, ip, html_file, cache_name,
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
                f"http://127.0.0.1:5001/{cloud_run_route}",
                data=json.dumps(payload, use_decimal=True),
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            res = rebuild_CalcVars(resp, form)

            res.html_vars['dataframe'] = convert_dataframe_var(res.html_vars['dataframe'])

            page = render_template(html_file, **res.html_vars)
            app.cache.set(cache_name, page)
            return page

        page = app.cache.get(cache_name)
        if page and not invalid_data_submitted:
            return page

        # else:
        return render_template(html_file, title='Home', form=form, data = None)


