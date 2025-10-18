from app import app, db
import pandas as pd
import itertools
from flask import g, url_for, request, redirect
from urllib.parse import urlparse
from flask_login import current_user
from datetime import datetime

# Add record to database from form calc data 'form' tied to given user 'user_id'
def add_calc_record(calc_name, form, ip, valid = True):
    extraneous = ['csrf_token', 'submit']
    data = {k:v for k,v in form.data.items() if k not in extraneous}
    data = {k:(float(v) if v.__class__.__name__ == 'Decimal' else v) for k,v in data.items()}
    data['valid'] = valid
    data['ip'] = ip
    data['user'] = current_user.get_id()
    data['datetime'] = datetime.utcnow()
    db.collection('calcs') \
        .document(calc_name) \
        .collection('calc') \
        .add(data)

def add_login_record(user_id, ip):
    db.collection('logins') \
        .add({'datetime':datetime.utcnow(), 'user':user_id, 'ip':ip})

# Load global variables to be used in template/routes etc
@app.before_request # call every time a request is made to site (hence can't make this code heavy)
def load_global_vars():
    # For randomising ordering groups so that each user sees investment models in a different order
    inv_models = {  'Peer to peer':('p2p_page', 'p2p'), # Name, (route, description-html-file-name)
                'Fund':('fund_page', 'fund'), 
                'Property':('property_page', 'property')} 
    inv_model_groups = list(itertools.permutations(list(inv_models)))
    num_groups = len(inv_model_groups) # e.g. for 3 investment models, there are 3! = 6 groups

    g.user_id = None # To be used by google analytics tracking
    if current_user.is_authenticated:
        userid = str(current_user.get_id())
        g.user_id = userid
        g.email = current_user.get_email()

        # Variables to support randomising order of investment models on pages
        group_num = ord(userid[0]) % num_groups # The randomising formula

    else:
        group_num = 0

    g.inv_models = [(x, url_for(inv_models[x][0])) for x in inv_model_groups[group_num]]
    g.inv_model_descs = ['content/home/' + inv_models[x][1] + '.html' for x in inv_model_groups[group_num]]
    pass

def redirect_to_next_page(app):
    with app.app_context():
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            return redirect(url_for('login_page'))
        return redirect(next_page)

def get_client_ip(app):
    with app.app_context():
        ips = request.headers.getlist("X-Forwarded-For")
        if ips:
            print('X-Forwarded-For')
            print(ips)
            ips = ips[0]
            return ips.split(', ')[0] if ', ' in ips else ips
        else:
            return request.remote_addr
    pass

def get_model_labels(group):
    df = pd.read_csv('form_fields.csv', usecols = ['group','name_df','label'])
    return df[df['group'] == group][['name_df', 'label']].set_index('name_df').to_dict()['label']