import investment_models.home_buying as home_buying
import investment_models.fund as fund
from investment_models.whatif.whatif_dfs import get_whatif_dfs
import pandas as pd
import os
from .lib import extract_descriptions, add_form_vars

class HomeBuyingVars():
    def __init__(self, form = None, itr = None):
        add_form_vars(obj = self, form = form, itr = itr)

    def parse_inputs(self):
        self.inputs = {
            'capital':int(self.capital),
            'sell_years':int(self.years),
            'property_cost':int(self.property_cost), 
            'mortgage_rate':float(self.mortgage_rate), 
            'mortgage_years':int(self.mortgage_years), 
            'property_growth':float(self.property_growth), 
            'buying_costs':int(self.net_buying_cost), 
            'fixed_selling_cost':int(self.fixed_selling_cost), 
            'sales_commission':float(self.sales_commission), 
            'annual_running_cost_perc':float(self.annual_running_cost_perc)
        }

    def get_summary(self):
        df_rent, rent_summary = fund.run(capital = float(self.capital), 
            years = int(self.years), 
            earnings = float(self.non_home_returns), 
            name = 'Rent home')
        self.summary = pd.concat([self.home_buying_summary, rent_summary], axis = 1)

    def get_rent_or_buy(self):
        self.metrics_descriptions = extract_descriptions('metrics', groups = ['base', 'cash'])
        self.rent_or_buy = 'rent' if self.summary.loc['Investment increase (%)', 'Rent home'] \
            > self.summary.loc['Investment increase (%)', 'Buy home'] else 'buy'

    def get_payback_period(self):
        a = self.summary['Buy home']['Payback period (years)']
        self.payback_period = a if type(a) != str else None

    def run(self):
        self.parse_inputs()

        self.home_buying_summary, self.df, self.principal, self.monthly_repayment = \
        home_buying.run(**self.inputs)

        self.get_summary()
        self.get_rent_or_buy()
        self.get_payback_period()

        # (Takes several seconds)
        self.whatif_dfs = get_whatif_dfs(
            model_inputs = self.inputs,
            specs = { # Configure whatif dfs (absolute/relative, num_datapoints)
                'property_growth':{'absolute':2},
                'annual_running_cost_perc':{'absolute':2},
                'mortgage_rate':{'absolute':2},
                'buying_costs':{'absolute':20000}
            },
            group = 'property',
            current_inputs = self.inputs,
            current_value = self.summary.loc['Final investment value', 'Buy home'],
            model_function = home_buying.home_investment) 
        
        return self
        
