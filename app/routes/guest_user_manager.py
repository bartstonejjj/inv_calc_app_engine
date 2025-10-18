from datetime import timedelta, datetime
from flask_login import current_user
from app import db
import pytz

# Will eventually be used to enhance freemium model, but not used currently.
def time_since_last_login(ip):
    last_login = Logins.query.filter_by(ip=ip).order_by(Logins.at.desc()).first()
    return datetime.utcnow() - last_login.at if last_login else timedelta.max

def calcs_count(ip, timeframe):

    ans = 0
    for calc_type in ['fund', 'p2p', 'property']:

        docs = db.collection('calcs').document(calc_type).collection('calc') \
            .where('ip', '==', ip).stream()
        
        num_docs = 0
        for doc in [d.to_dict() for d in docs]:
            if 'datetime' in doc:
                if doc['datetime'] > pytz.UTC.localize(datetime.utcnow() - timeframe):
                    if 'valid' in doc:
                        if doc['valid']:
                            num_docs += 1
        print(calc_type, 'calcs', num_docs)
        ans += num_docs
    return ans

def calc_quota_exceeded(ip, calc_quota, timeframe):
    return calcs_count(ip, timeframe) >= calc_quota

def is_guest_user(app):
    with app.app_context():
        print('current_user.id', current_user.get_id())
        return current_user.get_id() == 0

def guest_login_allowed(ip, calc_quota = 3, timeframe = timedelta(days = 1)):
    # return not calc_quota_exceeded(ip, calc_quota, timeframe)
    return True