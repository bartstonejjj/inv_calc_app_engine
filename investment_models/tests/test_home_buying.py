from pytest import approx
from ..home_buying import home_investment
from helpers.test_lib import *

property_cost = 500000
capital = 100000
mortgage_years = 25
rate = 4
property_growth = 6
buying_costs = 50000
fixed_selling_cost = 5000
sales_commission = 2
annual_running_cost_perc = 5

df, principal, monthly_repayment = home_investment(property_cost, capital, rate, mortgage_years, property_growth, 
    buying_costs, fixed_selling_cost, sales_commission, annual_running_cost_perc)

def test_home_investment_df():
    first = df.iloc[0]
    assert first['Regular Mortgage', 'Principal Paid'] == plus_minus_one(875)
    assert first['Regular Mortgage', 'Principal Remaining'] == plus_minus_five(449125)
    assert first['Property', 'Value'] == plus_minus_five(502500)
    assert first['Property', 'Total Selling Costs'] == plus_minus_five(15049)
    assert first['Property', 'Net Profit'] == plus_minus_five(-63768)
    assert first['Investment', 'Final investment value'] == plus_minus_five(36232)

    # Some of the below are given more tolerance since errors can trickle through whole model
    last = df.iloc[-1]
    assert last['Regular Mortgage', 'Principal Paid'] == plus_minus_one(2367)
    assert last['Regular Mortgage', 'Principal Remaining'] == approx_zero()
    assert last['Property', 'Value'] == plus_minus_five(2145935)
    assert last['Property', 'Total Selling Costs'] == plus_minus_five(47918)
    assert last['Property', 'Net Profit'] == plus_minus_five(581986)
    assert last['Investment', 'Final investment value'] == plus_minus_five(681986)

def test_principal():
    assert principal == plus_minus_five(450000)

def test_monthly_repayment():
    assert monthly_repayment == plus_minus_one(2375)

def test_doesnt_have_asset_cols():
    assert ('Investment', 'Final investment value (non-liquid)') not in df.columns
    assert ('Investment', 'Investment increase (non-liquid) (%)') not in df.columns
    assert ('Investment', 'Compound interest (non-liquid) (%)') not in df.columns