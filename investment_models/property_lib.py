import pandas as pd
from .comp_int import comp_int_loan, comp_int_future_value, comp_int_annual

def calculate_principal(property_cost, capital, buying_costs, fhog = 0):
    return property_cost - capital + buying_costs - fhog

def create_regular_mortgage_model(principal, rate, mortgage_years):
    df = comp_int_loan(principal, rate, mortgage_years)
    df.columns = pd.MultiIndex.from_product([['Regular Mortgage'], list(df.columns)])
    return df

# Limit to the number of months property will be owned (not neccessarily the loan period)
def get_months_owned(mortgage_years, sell_years = None):
    return (sell_years if sell_years else mortgage_years) * 12

def add_property_value(df, property_cost, property_growth, months_owned):
    df['Property', 'Value'] = comp_int_annual(capital = property_cost, 
                                            rate = property_growth, 
                                            years = months_owned // 12)['Balance']
    return df

def add_running_costs(df, annual_running_cost_perc):
    df['Property', 'Running Cost'] = (df['Property', 'Value'] * annual_running_cost_perc / 12 / 100).astype(int)
    df['Property', 'Accumulated Running Cost'] = df['Property', 'Running Cost'].cumsum()
    return df

def add_selling_costs(df, fixed_selling_cost, sales_commission):
    df['Property', 'Total Selling Costs'] = (fixed_selling_cost + df['Property', 'Value'] * sales_commission / 100).astype(int)
    return df