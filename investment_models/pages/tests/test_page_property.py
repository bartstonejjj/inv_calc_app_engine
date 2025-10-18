from investment_models.pages.property import HomeBuyingVars
from pytest import approx
from helpers.test_lib import *
import pandas as pd
from lib import unzip_names, FormData
from copy import deepcopy as copy

form_data = FormData(
capital= 100000, 
years = 10, 
property_cost = 500000, 
mortgage_rate = 4,
mortgage_years = 25, 
property_growth = 6, 
net_buying_cost = 35000, 
fixed_selling_cost = 5000,
sales_commission = 3, 
annual_running_cost_perc = 5,
non_home_returns = 9
)
v = HomeBuyingVars(itr = form_data.items()).run()

def test_summary_rent_home():
    assert v.summary['Rent home']['Payback period (years)'] == approx_zero()
    assert v.summary['Rent home']['Final investment value'] == plus_minus_five(236736)
    assert v.summary['Rent home']['Investment increase (%)'] == approx_percent(136.74)
    assert v.summary['Rent home']['Compound interest (%)'] == approx_percent(8.65)
    
def test_summary_buy_home():
    assert v.summary['Buy home']['Payback period (years)'] == approx_percent(3.75)
    assert v.summary['Buy home']['Final investment value'] == plus_minus_five(212982)
    assert v.summary['Buy home']['Investment increase (%)'] == approx_percent(112.98)
    assert v.summary['Buy home']['Compound interest (%)'] == approx_percent(7.58)

def test_metrics():
    assert set(unzip_names(v.metrics_descriptions)) == set(
        ['Payback period (years)', 
        'Final investment value', 
        'Investment increase (%)',
        'Compound interest (%)'])

def test_payback_period():
    assert v.payback_period == approx_percent(3.75)

def test_payback_period_null():
    fd = copy(form_data)
    fd.years = 1
    v = HomeBuyingVars(itr = fd.items()).run()
    assert v.payback_period == None

def test_rent_or_buy_for_rent():
    assert v.rent_or_buy == 'rent'

def test_rent_or_buy_for_buy():
    fd = copy(form_data)
    fd.property_growth = 7
    v = HomeBuyingVars(itr = fd.items()).run()
    assert v.rent_or_buy == 'buy'