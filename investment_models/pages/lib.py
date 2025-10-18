import os
import pandas as pd

def extract_descriptions(csv, groups):
    df = pd.read_csv(os.getcwd() + '/' + csv + '.csv')
    df = df[df['group'].isin(groups)]
    df = df[['label', 'description']]
    return zip(df['label'], df['description'])

def form_field_iter(form):
    extraneous = ['csrf_token', 'submit']
    form_fields = {k:v for k,v in form.data.items() if k not in extraneous}
    for name, value in form_fields.items():
        yield name, value

def add_form_vars(obj, form = None, itr = None):
    for name, value in (itr if itr else form_field_iter(form)):
        setattr(obj, name, value)
