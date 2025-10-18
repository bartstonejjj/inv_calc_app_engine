import pandas as pd
from investment_models.lib import pretty_model
from .inv_totals import add_ROI, inv_summary
from .property_lib import *
from .comp_int import monthly_repayment
from pytest import approx

# Buy property to live in, what for capital growth
# ** Input parameters **
# property_cost = initial cost of purchasing property
# captial = amount of money initally invested in the property
# mortgage_rate = interest rate of mortgage
# mortgage_years = length of the mortgage
# sell_years = number of years after buying is the property is sold [must be integer]
# property_growth = estimated annual growth of property's value
# fhog = First Home Owner's Grant
# buying costs defaults estimated from: 
#     http://www.yourmortgage.com.au/article/tallying-up-all-the-costs-of-buying-a-home-79472.aspx
# selling commission and costs (see below) defaults estimated from: 
#     https://www.finder.com.au/selling-your-home-online (2500 fo repair costs)
# fixed_selling_costs - all selling costs that are not estate agent commission
# Notes - For simplicity, we assume that the monthly cost of mortgage repayments is roughly the same as what you will pay in rent,
# hence accumulated interest (which is part of monthly repayment) is not considered as a cost for the purpose of this calculation.
def home_investment(property_cost, capital, mortgage_rate, mortgage_years, property_growth, 
    buying_costs, fixed_selling_cost, sales_commission, 
    annual_running_cost_perc, sell_years = None, fhog = 0):
    
    principal = calculate_principal(property_cost, capital, buying_costs, fhog)
    df = create_regular_mortgage_model(principal, mortgage_rate, mortgage_years)

    months_owned = get_months_owned(mortgage_years, sell_years)
    df = df.head(months_owned)  
    
    df = add_property_value(df, property_cost, property_growth, months_owned)
    df = add_running_costs(df, annual_running_cost_perc)
    df = add_selling_costs(df, fixed_selling_cost, sales_commission)

    df['Property', 'Revenue from sale'] = df['Property', 'Value'] \
    - df['Regular Mortgage', 'Principal Remaining'] \
    - df['Property', 'Total Selling Costs']

    df['Property', 'Net Profit'] = df['Property', 'Revenue from sale'] \
    - capital \
    - df['Property', 'Accumulated Running Cost']
        
    df = add_ROI(df, capital, df['Property', 'Net Profit'] + capital, add_asset_cols = False)

    monthly_repayment = df.iloc[0]['Regular Mortgage', 'Principal Paid'] + \
        df.iloc[0]['Regular Mortgage', 'Interest Paid']
    return df, principal, monthly_repayment

def run(*args, **kwargs):
    df, principal, monthly_repayment = home_investment(**kwargs)
    summary = inv_summary(df, 'Buy home')
    return summary, pretty_model(df), principal, monthly_repayment
