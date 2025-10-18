from app import firebase
from requests.exceptions import HTTPError
from firebase_admin import auth as admin_auth, exceptions as admin_exceptions

# Initialize the Pyrebase auth service once
auth_client = firebase.auth()

def parse_http_error(error):
    response = error.args[0].response
    error = str(response.json()['error']['message'])
    print(error)
    
    error_parts = [x.strip() for x in error.split(':')]
    error = error_parts[0]
    additional_error_info = (error_parts[1] + '.' if len(error_parts) > 1 else '').replace('..','.')
    
    user_message = {
        'WEAK_PASSWORD':'Please enter a valid password.',
        'INVALID_EMAIL':'Please enter a valid email address.',
        'EMAIL_EXISTS':'Email exists, please log in if this is your email address.',
        'INVALID_PASSWORD':'Email or password incorrect, please try again.',
        'EMAIL_NOT_FOUND':'Email or password incorrect, please try again.',
        'TOO_MANY_ATTEMPTS_TRY_LATER': None
        }
    error_code = error if error in user_message else None

    return error_code, ' '.join(filter(None,
        [user_message[error_code] if error_code else None, additional_error_info]))

def try_firebase_user_task(function):
    def wrapper(email, password):
        try:
            user = function(email, password)

        except HTTPError as error:
            return (None,) + parse_http_error(error)

        return user, None, None

    return wrapper

@try_firebase_user_task
def try_create_user(email, password):
    return auth_client.create_user_with_email_and_password(email, password)

@try_firebase_user_task
def try_sign_in_user(email, password):
    return auth_client.sign_in_with_email_and_password(email, password)

def try_get_user_by_email(email):
    user = None
    try:
        user = admin_auth.get_user_by_email(email)
        user = user.__dict__
        user = user['_data']
    except admin_exceptions.FirebaseError:
        return None
    return user