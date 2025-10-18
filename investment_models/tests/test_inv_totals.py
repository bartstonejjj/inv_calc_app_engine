from ..inv_totals import add_ROI
import pandas as pd
from helpers.test_lib import *

capital = 10000

# Create empty dataframe 'Dummy Model' that has final balance of:
#   414 at month 2 (i.e. negative earnings)
#   13352 at month 60
df = pd.DataFrame(columns = ['Balance'], index = [1,59], data = [414, 13352]) 
df.columns = pd.MultiIndex.from_product([['Dummy Model'], list(df.columns)])
df = add_ROI(df, capital, bal_end = df['Dummy Model', 'Balance'])

def test_add_roi():
    assert df['Investment', 'Final investment value'].iloc[-1] == plus_minus_one(13352)
    assert df['Investment', 'Investment increase (%)'].iloc[-1] == approx_percent(33.52)
    assert df['Investment', 'Compound interest (%)'].iloc[-1] == approx_percent(5.80)

def test_add_roi_for_negative_ci_equiv():
    assert df['Investment', 'Compound interest (%)'].iloc[0] == approx_percent(-479.4)