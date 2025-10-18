from investment_models.whatif.lib import *
from investment_models.home_buying import home_investment
from pandas.util.testing import assert_series_equal
import pandas as pd
import numpy as np

def test_get_datapoints():
    value = 1000
    min = 0
    max = 3000
    num_datapoints = 5 # actual number of datapoints is output is often 1 less, since value is excluded.
    dtype = int

    assert get_datapoints(value, min, max, num_datapoints, dtype, relative = 0.1) == \
        [900, 950, 1050, 1100] # Value excluded from output

    assert get_datapoints(value, min, max, num_datapoints, dtype, absolute = 100) == \
        [900, 950, 1050, 1100] # Value excluded from output

    num_datapoints = 4
    assert get_datapoints(value, min, max, num_datapoints, dtype, absolute = 75) == \
        [925, 975, 1025, 1075] # Doesn't include 'value'        

    num_datapoints = 5
    assert get_datapoints(value, min, max, num_datapoints, dtype, absolute = 100, rounding = -2) == \
        [900, 1100] # Fewer datapoints since the rounding caused (removed) duplicates

    min = 900
    assert get_datapoints(value, min, max, num_datapoints, dtype, absolute = 500) == \
        [900, 1050, 1200, 1350, 1500] 

    get_datapoints(value, min, max, num_datapoints, dtype, absolute = 500) == \
        [1000]  # Fewer datapoints since they don't fix min/max criteria

def test_data_points_overriding_min_max():
    assert get_datapoints(value = 1, min = 1, max = 50, num_datapoints = 5, dtype = int, absolute = 500) == \
        [13, 25, 37, 50]

    assert get_datapoints(value = 50, min = 1, max = 50, num_datapoints = 5, dtype = int, absolute = 500) == \
        [1, 13, 25, 37]

def test_InvestmentMany_for_home_investment():
    dic = \
    {'property_cost':500000,
    'capital':100000,
    'mortgage_years':25,
    'mortgage_rate':4,
    'sell_years':10,
    'property_growth':6,
    'buying_costs':50000,
    'fixed_selling_cost':5000,
    'sales_commission':2,
    'annual_running_cost_perc':5,
    'function':home_investment,
    'investment_field':'Final investment value',
    'investment_field_type':np.int64}
    df = InvestmentMany(**dic).run(field_to_vary = 'property_cost', min = 0, max = 1000000, dtype = int,
                                     relative = 0.4, num_datapoints = 6, rounding = -5)
    
    assert_series_equal(df['property_cost'], pd.Series([300000, 400000, 600000, 700000], 
        name = 'property_cost'))
    assert_series_equal(df['Final investment value'], pd.Series([139032, 175130, 247318, 283423],
        name = 'Final investment value'))