import pandas as pd
from pytest import approx
from ..fund import *
from helpers.test_lib import *

capital = 10000
earnings = 8.3
mgmt_fee = 0.44
annual_fee = 0
years = 10
df = fund(capital, years, earnings, mgmt_fee, annual_fee)

def test_fund():
    assert df.iloc[0]['Investment', 'Compound interest (%)'] == approx_percent(7.83)
    assert df.iloc[0]['Fund', 'Balance net of fees'] == plus_minus_five(10065)
    assert df.iloc[-1]['Investment', 'Compound interest (%)'] == approx_percent(7.56)
    assert df.iloc[-1]['Fund', 'Balance net of fees'] == plus_minus_five(21243)

def test_fund_with_mgmt_and_annual_fees():
    df = fund(capital, years, earnings, mgmt_fee, annual_fee = 100)
    assert df.iloc[0]['Investment', 'Compound interest (%)'] == approx_percent(6.72)
    assert df.iloc[0]['Fund', 'Balance net of fees'] == plus_minus_five(10056)
    assert df.iloc[-1]['Investment', 'Compound interest (%)'] == approx_percent(6.86)
    assert df.iloc[-1]['Fund', 'Balance net of fees'] == plus_minus_five(19809)