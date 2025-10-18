import os

def get_vars():
    return dict(os.environ)

def get_vars_subset(subset):
    return {k:v for k,v in get_vars().items() if k in subset}

def get_pyrebase_vars():
    tmp = get_vars_subset(subset = ['APIKEY', 'AUTHDOMAIN', 'DATABASEURL', 'STORAGEBUCKET'])
    ans = {}
    ans['apiKey'] = tmp['APIKEY']
    ans['authDomain'] = tmp['AUTHDOMAIN']
    ans['databaseURL'] = tmp['DATABASEURL']
    ans['storageBucket'] = tmp['STORAGEBUCKET']
    del tmp
    return ans