import pandas as pd
import numpy as np
from .pandas_lib import series_has_data, series_from_index

def ci_equiv(series, capital):
    sign = series.map(lambda x: -1 if x < capital else 1) # -ve if decreased from captial, +ve otherwise

    increase = abs((series - capital)/capital)
    
    series = round(((increase + 1).pow(1 / (series_from_index(series) + 1)) - 1) * 12 * 100, 2)
    return series * sign

# Add fields related to how well the investment performed over time.
def add_ROI(df, capital, bal_end, asset_bal_end = None, add_asset_cols = True):
    capital = float(capital)
    
    def increase(series):
        return round(100 * (series - capital) / capital, 2)
    
    def get_variables(series):
        return (series, increase(series), ci_equiv(series, capital)) if series_has_data(series) \
            else (np.nan, np.nan, np.nan)
    
    a, b, c = get_variables(bal_end)
    df['Investment', 'Final investment value'] = a
    df['Investment', 'Investment increase (%)'] = b
    df['Investment', 'Compound interest (%)'] = c

    if add_asset_cols:
        a, b, c = get_variables(asset_bal_end)
        df['Investment', 'Final investment value (non-liquid)'] = a
        df['Investment', 'Investment increase (non-liquid) (%)'] = b
        df['Investment', 'Compound interest (non-liquid) (%)'] = c
    
    return df

# Calculate the payback period in years
def calc_payback_period(df):
    cash_inc = df[df['Investment', 'Investment increase (%)'] >= 0] # Dataframe for only years with cash increase
    return round(cash_inc.reset_index()['index'].min() / 12, 2) if len(cash_inc) > 0 else np.nan

# Output summary of investment based on key metrics as a series. E.g.
    # Payback period (years)        0.00
    # Cash Balance                    11616.00
    # Cash Increase (ROI) (%)                       16.16
    # Cash CI_Equiv (%)                   3.00
    # Asset Balance
    # Asset Increase (%)
    # Asset CI_Equiv
def inv_summary(df, inv_name):
    a = pd.Series(calc_payback_period(df), ['Payback period (years)']).to_frame()
    a.columns = [inv_name]
    b = df.iloc[-1]['Investment'].to_frame()
    b.columns = [inv_name]

    df = pd.concat([a, b], axis=0)
    return df.fillna('-')