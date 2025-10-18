import pandas as pd
import numpy as np
from investment_models.lib import pretty_model
from .inv_totals import add_ROI, inv_summary
from .comp_int import comp_int_annual

def fund_balance_and_fees_paid(capital, earnings, mgmt_fee, annual_fee):
    earning_value = capital * (1 + earnings / 100)
    fund_balance = earning_value / (1 + mgmt_fee / 100) - annual_fee
    return round(fund_balance)

def update_balances(df, year, earnings, mgmt_fee, annual_fee):
    fund_balance = fund_balance_and_fees_paid(df.loc[year, 'start'], earnings, mgmt_fee, annual_fee)
    df.loc[year, 'end'] = fund_balance

# fee = management fee % - which is the average value of the asset throughout year * total fees
# earnings = estimated % increase in fund value per years throughout all years
def fund(capital, years, earnings, mgmt_fee = 0, annual_fee = 0):
    df = pd.DataFrame(columns = ['start', 'end'])

    df['year'] = list(range(1, years + 1))
    df = df.set_index('year')

    df.loc[1, 'start'] = round(capital)
    update_balances(df, year = 1, earnings = earnings, mgmt_fee = mgmt_fee, annual_fee = annual_fee)

    for year in range(2, years + 1):
        df.loc[year, 'start'] = df.loc[year - 1, 'end']
        update_balances(df, year = year, earnings = earnings, mgmt_fee = mgmt_fee, annual_fee = annual_fee)

    # Create month and year dataframe
    m = pd.DataFrame(data = list(range(1, years * 12 + 1)), columns = ['month'])
    m['year'] = m['month'].map(lambda x: x // 12 + 1 if x % 12 == 1 else np.nan)

    # Convert year dataframe to month dataframe through interpolation
    df = df.merge(m, left_index = True, right_on = 'year', how = 'right')
    df.loc[years * 12, 'start'] = df.loc[df['year'] == years, 'end'].iloc[0]
    df['start'] = df['start'].astype(float).interpolate().astype(int)

    df['end'] = df['start'].shift(-1)
    df['year'] = df['year'].ffill()
    df = df[:-1] # extraneous last column

    df = df.rename(columns = {'end':'Balance net of fees'})

    # Do a simple annual compound interest model
    df['Zero fee earnings'] = \
        comp_int_annual(capital = capital, 
            rate = earnings, 
            years = years, 
            deposits = None)['Balance'].astype(int)

    # This is both the fee paid as well as the loss of income from the compound interest it would produce
    df['Accumulated effect of fees'] = df['Zero fee earnings'] - df['Balance net of fees']

    df = df[['Zero fee earnings', 'Accumulated effect of fees', 'Balance net of fees']]
    
    df.columns = pd.MultiIndex.from_product([['Fund'], list(df.columns)])

    return add_ROI(df, capital, bal_end = df['Fund', 'Balance net of fees'], add_asset_cols = False)

def run(*args, name = 'Fund', **kwargs):
    df = fund(*args, **kwargs)
    summary = inv_summary(df, name)
    return pretty_model(df), summary