import pandas as pd
from pytest import approx
from ..p2p import *
from helpers.test_lib import *

capital = 10000
years = 5
p2p_rate = 9 
savings_rate = 3

def test_p2p_reinvest_savings_acc():
    df = p2p_reinvest_savings_acc(capital, years, p2p_rate, savings_rate)
    assert df.iloc[-1]['Investment', 'Compound interest (%)'] == approx_percent(5.8)
    assert pd.isnull(df.iloc[-1]['Investment', 'Compound interest (non-liquid) (%)'])

def test_p2p_reinvest_p2p():
    df = p2p_reinvest_p2p(capital, years, p2p_rate)
    assert pd.isnull(df.iloc[-1]['Investment', 'Compound interest (%)'])
    assert df.iloc[-1]['Investment', 'Compound interest (non-liquid) (%)'] == approx_percent(9)

def test_p2p_no_reinvest():
    df = p2p_no_reinvest(capital, years, p2p_rate)
    assert df.iloc[-1]['Investment', 'Compound interest (%)'] == approx_percent(4.4)
    assert pd.isnull(df.iloc[-1]['Investment', 'Compound interest (non-liquid) (%)'])