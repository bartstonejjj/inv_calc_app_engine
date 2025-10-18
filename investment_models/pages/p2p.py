import investment_models.p2p as p2p
import investment_models.savings as savings
import pandas as pd
import os
from .lib import extract_descriptions, add_form_vars

class P2PVars():
    def __init__(self, form = None, itr = None):
        add_form_vars(obj = self, form = form, itr = itr)

    def run(self):
        self.df_p2p, p2p_summary = p2p.run(capital = float(self.capital), years = int(self.years), 
            p2p_rate = float(self.p2p_rate), savings_rate = float(self.savings_rate))

        df_sav, sav_summary = savings.run(capital = float(self.capital), rate = float(self.savings_rate),
            years = int(self.years))

        self.summary = pd.concat([sav_summary, p2p_summary], axis = 1)
        self.summary.columns = pd.MultiIndex.from_product([['Investments'], list(self.summary.columns)])
        self.s_p2p_reinvest_savings = p2p_summary['P2P reinvest into savings']
        self.metrics_descriptions = extract_descriptions('metrics', groups = ['base', 'cash', 'asset'])
        self.investments_descriptions = extract_descriptions('investments', groups = ['p2p'])
        return self
        
