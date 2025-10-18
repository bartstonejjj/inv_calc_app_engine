from investment_models.pages.p2p import P2PVars
from pytest import approx
from helpers.test_lib import *
import pandas as pd
from lib import unzip_names

form_data = [('capital', 10000), ('years', 5), ('savings_rate', 3), ('p2p_rate', 9)]
v = P2PVars(itr = form_data).run()

def test_summary_savings():
    a, b = 'Investments', 'Savings Account'
    assert v.summary[a, b]['Payback period (years)'] == approx_zero()
    assert v.summary[a, b]['Final investment value'] == plus_minus_five(11616)
    assert v.summary[a, b]['Investment increase (%)'] == approx_percent(16.16)
    assert v.summary[a, b]['Compound interest (%)'] == approx_percent(3)
    assert are_NA([v.summary[a, b][x] for x in \
        ['Final investment value (non-liquid)', 'Investment increase (non-liquid) (%)', 'Compound interest (non-liquid) (%)']])

def test_summary_p2p_reinvest_savings():
    a, b = 'Investments', 'P2P reinvest into savings'
    assert v.summary[a, b]['Payback period (years)'] == approx_percent(3.75)
    assert v.summary[a, b]['Final investment value'] == plus_minus_five(13352)
    assert v.summary[a, b]['Investment increase (%)'] == approx_percent(33.52)
    assert v.summary[a, b]['Compound interest (%)'] == approx_percent(5.8)
    assert are_NA([v.summary[a, b][x] for x in \
        ['Final investment value (non-liquid)', 'Investment increase (non-liquid) (%)', 'Compound interest (non-liquid) (%)']])

def test_summary_p2p_reinvest_p2p():
    a, b = 'Investments', 'P2P reinvest into P2P'
    assert v.summary[a, b]['Final investment value (non-liquid)'] == plus_minus_five(15656)
    assert v.summary[a, b]['Investment increase (non-liquid) (%)'] == approx_percent(56.56)
    assert v.summary[a, b]['Compound interest (non-liquid) (%)'] == approx_percent(9)
    assert are_NA([v.summary[a, b][x] for x in \
        ['Final investment value', 'Investment increase (%)', 'Compound interest (%)']])

def test_summary_p2p_reinvest_savings():
    a, b = 'Investments', 'P2P with no reinvest'
    assert v.summary[a, b]['Payback period (years)'] == approx_percent(4)
    assert v.summary[a, b]['Final investment value'] == plus_minus_five(12454)
    assert v.summary[a, b]['Investment increase (%)'] == approx_percent(24.54)
    assert v.summary[a, b]['Compound interest (%)'] == approx_percent(4.4)
    assert are_NA([v.summary[a, b][x] for x in \
        ['Final investment value (non-liquid)', 'Investment increase (non-liquid) (%)', 'Compound interest (non-liquid) (%)']])

def test_s_p2p_reinvest_savings():
    assert v.s_p2p_reinvest_savings['Payback period (years)'] == approx_percent(3.75)
    assert v.s_p2p_reinvest_savings['Final investment value'] == plus_minus_five(13352)
    assert v.s_p2p_reinvest_savings['Investment increase (%)'] == approx_percent(33.52)
    assert v.s_p2p_reinvest_savings['Compound interest (%)'] == approx_percent(5.8)

def test_metrics():
    assert set(unzip_names(v.metrics_descriptions)) == set(
        ['Payback period (years)', 
        'Final investment value', 
        'Investment increase (%)',
        'Compound interest (%)', 
        'Final investment value (non-liquid)', 
        'Investment increase (non-liquid) (%)', 
        'Compound interest (non-liquid) (%)'])

def test_investments():
    assert set(unzip_names(v.investments_descriptions)) == set(
        ['Savings Account', 
        'P2P reinvest into savings',
        'P2P reinvest into P2P', 
        'P2P with no reinvest'])