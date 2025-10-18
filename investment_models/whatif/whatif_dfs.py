from investment_models.whatif.lib import *
import numpy as np

from copy import deepcopy as copy

def get_fields(group):
    df = pd.read_csv('form_fields.csv', usecols = ['group','name_df','min', 'max', 'type'])
    return df[df['group'] == group]

def get_investment_many(model_inputs, model_function):
    flds = model_inputs
    flds['function'] = model_function
    flds['investment_field'] = 'Final investment value'
    flds['investment_field_type'] = np.int64
    print(flds)
    return InvestmentMany(**flds)

def get_what_if_spec(specs, field):
    spec = specs[field]

    # Set defaults
    for key in ['relative', 'absolute']:
        if key not in spec:
            spec[key] = None
    if 'num_datapoints' not in spec:
        spec['num_datapoints'] = 2 # Configuration for default num_datapoints
    
    return spec

def fields_details(specs, group):
    df = get_fields(group)
    df = df[df['name_df'].isin(specs.keys())]
    dtypes = {'IntegerField':int, 'DecimalField':float}

    for i, row in df.iterrows():
        spec = get_what_if_spec(specs, row['name_df'])
        yield {
            **{
            'field_to_vary': row['name_df'],
            'min':row['min'],
            'max':row['max'],
            'dtype':dtypes[row['type']]
            },
            **spec
        }

def calculate_whatif_dfs(model_inputs, specs, group, model_function):
    ans = {}
    for field_details in fields_details(specs, group):
        print('Running whatif for')
        print(field_details)
        ans[field_details['field_to_vary']] = \
            get_investment_many(copy(model_inputs), model_function).run(**field_details)
        print()
    return ans

def add_value_to_whatif_dfs(whatif_dfs, inputs, value):
    ans = {}
    for name, df in whatif_dfs.items():
        # create a one-row DataFrame for the new record
        new_row = pd.DataFrame([{name: inputs[name], "Final investment value": value}])
        # concat replaces the old append
        df = pd.concat([df, new_row], ignore_index=True)

        ans[name] = (
            df.sort_values(by=name)
              .reset_index(drop=True)
              .to_json()
        )
    return ans


def get_whatif_dfs(model_inputs, specs, group, current_inputs, current_value, model_function):

    whatif_dfs = calculate_whatif_dfs(model_inputs, specs, group, model_function)
    
     # Add current values to whatif_dfs
    whatif_dfs = add_value_to_whatif_dfs(whatif_dfs, 
        inputs = current_inputs, 
        value = current_value)
    return whatif_dfs
