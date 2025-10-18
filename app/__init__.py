import sys
import types
import os

# -------------------------------------------------------------------
# Compatibility patches for legacy Pyrebase4 + requests-toolbelt
# -------------------------------------------------------------------
try:
    import requests
    import urllib3
    fake_contrib = types.ModuleType("requests.packages.urllib3.contrib.appengine")
    fake_contrib.is_appengine_sandbox = lambda: False
    sys.modules["requests.packages.urllib3.contrib.appengine"] = fake_contrib
except Exception as e:
    print("⚠️  Could not patch requests.appengine:", e)

try:
    import requests_toolbelt._compat as _compat
    if not hasattr(_compat, "gaecontrib"):
        _compat.gaecontrib = types.SimpleNamespace()
except Exception as e:
    print("⚠️  Could not patch requests_toolbelt._compat.gaecontrib:", e)

# -------------------------------------------------------------------
# Google Cloud Debugger (optional)
# -------------------------------------------------------------------
try:
    import googleclouddebugger
    googleclouddebugger.enable()
except ImportError:
    pass

# -------------------------------------------------------------------
# Flask and extensions
# -------------------------------------------------------------------
from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_caching import Cache

# -------------------------------------------------------------------
# Firebase / Firestore
# -------------------------------------------------------------------
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
from app.env_vars import get_pyrebase_vars

# -------------------------------------------------------------------
# App setup
# -------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config.get("SECRET_KEY", os.environ.get("SECRET_KEY", "dev-fallback-key"))


# Firebase Admin SDK
firebase_admin.initialize_app(
    credentials.ApplicationDefault(),
    {"projectId": app.config.get("PROJECT_ID")}
)

db = firestore.client()

# Pyrebase client
firebase = pyrebase.initialize_app(get_pyrebase_vars())
firebase_auth = firebase.auth()

# Flask extensions
login = LoginManager(app)
login.login_view = "login"
login.login_message = None

bootstrap = Bootstrap(app)
mail = Mail(app)
app.cache = Cache(app)
from markdown import markdown  # lowercase function, not a class

# -------------------------------------------------------------------
# Import routes and models
# -------------------------------------------------------------------
from app import models
from app.routes import main_routes
