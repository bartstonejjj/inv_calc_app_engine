import pandas as pd
from investment_models.inv_totals import add_ROI, inv_summary
from investment_models.comp_int import comp_int, comp_int_loan
from investment_models.lib import pretty_model

# Invest in peer to peer lending, re-invest monthly capital/interest into savings account
# Parameters as per above: comp_int, comp_int_loan
# totals = True if you want to see totals (will need to provide salary), False otherwise
# salary =  annual gross salary
def p2p_reinvest_savings_acc(capital, years, p2p_rate, savings_rate):

    rs = comp_int_loan(capital, p2p_rate, years, additional_payments = pd.Series([0] * years * 12), p2p = True) # RateSetter dataframe, no monthly deposits to loan
    sa = comp_int(0, savings_rate, years, rs['Capital Repaid'] + rs['Interest Received']) # Savings Acount dataframe
    
    # Add top level label to said columns
    rs.columns = pd.MultiIndex.from_product([['P2P'], list(rs.columns)])
    sa.columns = pd.MultiIndex.from_product([['Savings Account'], list(sa.columns)])
    
    # Join tables together
    df = pd.concat([rs, sa], axis = 1).reset_index(drop = True)
    
    df = df.astype(int)
    
    df = add_ROI(df, capital, df['Savings Account', 'Balance']) 

    return df

# Invest in peer to peer lending, re-invest monthly capital/interest into more peer loans
def p2p_reinvest_p2p(capital, years, p2p_rate):

    df = comp_int(capital = capital, rate = p2p_rate, years = years)

    df.columns = pd.MultiIndex.from_product([['P2P'], list(df.columns)])
    
    df = df.astype(int)
    
    df = add_ROI(df, capital, bal_end = None, asset_bal_end = df['P2P', 'Balance']) 

    return df

# Invest in peer to peer lending and nothing else. Just leave the money in holding account
def p2p_no_reinvest(capital, years, p2p_rate):

    df = comp_int_loan(principal = capital, rate = p2p_rate, years = years)
    
    df['Balance'] = df['Accumulated Interest'] + capital - df['Principal Remaining']

    df.columns = pd.MultiIndex.from_product([['P2P'], list(df.columns)])
    
    df = df.astype(int)
    
    df = add_ROI(df, capital, bal_end = df['P2P', 'Balance']) 

    return df

# Run peer to peer models and output: example model (as df), and summary table
def run(capital, years, p2p_rate, savings_rate):
    p2p_sav = p2p_reinvest_savings_acc(capital, years, p2p_rate, savings_rate)
    p2p_p2p = p2p_reinvest_p2p(capital, years, p2p_rate)
    p2p = p2p_no_reinvest(capital, years, p2p_rate)

    return pretty_model(p2p_sav), pd.concat(
        [inv_summary(p2p_sav, 'P2P reinvest into savings'), 
        inv_summary(p2p_p2p, 'P2P reinvest into P2P'),
        inv_summary(p2p, 'P2P with no reinvest')], axis = 1)
