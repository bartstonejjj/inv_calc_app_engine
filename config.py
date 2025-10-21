import os
import yaml

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Add all env_variables from app.yaml
    env_vars = yaml.safe_load((open(os.path.join(basedir, 'app.yaml'))))['env_variables']
    for name, var in env_vars.items():
        locals()[name] = var

    # Check if this is running locally or in prod (need to have set FLASK_LOCAL=1 manually)
    LOCAL = os.environ.get('FLASK_LOCAL') or False

    PROJECT_ID = 'inv-calc-gcp'

    CACHE_TYPE = "simple" # Flask-Caching related configs

    CLOUD_RUN_KEY = '2498fhijwfnjkf8934quhdsjkbsd40woawrgkjnfsjweaf09rohawfjafjkjfdskj'
    CLOUD_RUN_URL = 'https://inv-calc-cloud-run-7jm66aytua-ts.a.run.app'
    # CLOUD_RUN_URL = 'http://127.0.0.1:5001' # local use only