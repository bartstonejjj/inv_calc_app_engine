import investment_models.fund as fund
import pandas as pd
import os
from .lib import extract_descriptions, add_form_vars
from investment_models.whatif.whatif_dfs import get_whatif_dfs

class FundVars():
    def __init__(self, form = None, itr = None):
        add_form_vars(obj = self, form = form, itr = itr)

    def parse_inputs(self):
        self.inputs = {
            'capital':int(self.capital),
            'years':int(self.years),
            'earnings':float(self.earnings), 
            'mgmt_fee':float(self.mgmt_fee), 
            'annual_fee':float(self.annual_fee) 
        }

    def run(self):
        self.parse_inputs()

        self.df, self.summary = fund.run(capital = float(self.capital), years = int(self.years), 
            earnings = float(self.earnings), mgmt_fee = float(self.mgmt_fee), 
            annual_fee = float(self.annual_fee))

        self.s_fund = self.summary['Fund']
        self.metrics_descriptions = extract_descriptions('metrics', groups = ['base', 'cash'])

        self.whatif_dfs = get_whatif_dfs(
            model_inputs = self.inputs,
            specs = { # Configure whatif dfs (absolute/relative, num_datapoints)
                'earnings':{'absolute':5},
                'mgmt_fee':{'absolute':2},
                'annual_fee':{'absolute':200}
            },
            group = 'fund',
            current_inputs = self.inputs,
            current_value = self.summary.loc['Final investment value', 'Fund'],
            model_function = fund.fund)

        return self