# To help with running 'What If' Analyses
import pandas as pd
import numpy as np

def get_start_end(value, minn, maxx, relative, absolute):
    if relative:
        start = value * (1 - relative)
        end = value * (1 + relative)
    else:
        start = value - absolute
        end = value + absolute
    return max(minn, start), min(maxx, end)

def get_datapoints(value, min, max, num_datapoints, dtype, relative = None, absolute = None, rounding = 1):

    start, end = get_start_end(value, min, max, relative, absolute)

    lst = sorted(list(set([round(dtype(x), rounding) for x in np.linspace(start, end, num_datapoints)])))
    value = round(dtype(value), rounding)
    if value in lst:
        lst.remove(value)
    return lst

class InvestmentMany(object):
    def __init__(self, **kwargs):
        self.function = kwargs['function']
        self.investment_field = kwargs['investment_field']
        self.investment_field_type = kwargs['investment_field_type']
        del kwargs['function'], kwargs['investment_field'], kwargs['investment_field_type']
        self.kwargs = kwargs
    
    def run(self, field_to_vary, min, max, num_datapoints, dtype, relative = None, absolute = None, rounding = 1):
        df = pd.DataFrame()
        df[field_to_vary] = get_datapoints(self.kwargs[field_to_vary], min, max, num_datapoints, dtype,
                                           relative, absolute, rounding)
        print(df)
        df[self.investment_field] = 0
        
        for value in df[field_to_vary]:
            self.kwargs[field_to_vary] = value

            # Get output dataframe of function 
            # (which is the either direct output first value of the packed tuple outputs)
            function_outputs = self.function(**self.kwargs)
            function_output = function_outputs[0] if type(function_outputs) == tuple else function_outputs

            df.loc[df[field_to_vary]==value, self.investment_field] = \
                function_output.iloc[-1]['Investment'][self.investment_field]

        df[self.investment_field] = df[self.investment_field].astype(self.investment_field_type)
        return df.reset_index(drop = True)