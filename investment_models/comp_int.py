import pandas as pd
import numpy as np
from .pandas_lib import series_has_data, insert_blank_lines

# Calculate the future value of monthly compound interest, with annual rate % 'rate' and 
def comp_int_future_value(present_value, rate, num_months):
    return present_value * (1 + rate / 12 / 100) ** num_months

# Calculate the monthly repayment of loan with 'principal', 'rate' over the course of 'num_months' months
def monthly_repayment(principal, rate, num_months):
    r = rate/12/100
    n = num_months
    return principal * r * (1 + r)**n / ((1 + r)**n - 1)

# General compound interest model that could be used for annual or monthly compounding
def comp_int_general(capital, rate, years, monthly_compound, deposits = None):
    month_factor = 12 if monthly_compound else 1

    deposits = deposits if series_has_data(deposits) else pd.Series([0] * years * month_factor)

    # Calculate first row values
    vals = {}
    vals['Interest Received'] = round(capital * rate / 100 / month_factor, 2)
    vals['Balance'] = capital + vals['Interest Received'] + deposits.iloc[0]

    # Create dataframe and add first row values
    df = pd.DataFrame([vals])

    # Add all remaining (derived) rows to dataframe
    for i in range(1, years * month_factor):

        # Apply interest on final balance of previous month
        vals['Interest Received'] = round(float(df.loc[i - 1, 'Balance']) * rate / 100 / month_factor, 2) 
        
        # Add to previous months final balance, this month's interest and deposit amount
        vals['Balance'] = float(df.loc[i - 1, 'Balance']) + vals['Interest Received'] + deposits.iloc[i] 
        
        df = pd.concat([df, pd.DataFrame([vals])], ignore_index=True)
        
    df['Deposits'] = deposits
    
    # Summing the total cumulative interest at end of each month
    df['Accumulated Interest'] = df['Interest Received'].cumsum()

    # Re order columns
    df = df[['Deposits', 'Interest Received', 'Balance', 'Accumulated Interest']]
    return df

# Compound interest  model to generate monthly values in a dataframe
#
# Input parameters
# --
# LENGTH OF LOAN/INVESTMENT:
# capital - the initial amount invested
# rate - the annual interest of the fixed rate loan as %
# years - the numer of years of the loan
# --
# EACH MONTH (series values):
# deposits - the amount of money added each month (on top of interest earnt)
# --
# Output columns
# --
# EACH MONTH:
# Interest Received - interest received in this month
# Balance - the balance at end of month
# Accumulated Interest - total interest paid/received end of month
def comp_int(capital, rate, years, deposits = None):
    return comp_int_general(capital, rate, years, monthly_compound = True, deposits = deposits)


def fill_exponential_balance(df, annual_growth_rate, start_balance):
    """
    Fill 'Balance' column using exponential monthly growth, starting from a known initial value.

    annual_growth_rate: e.g. 0.06 for 6% annual growth
    start_balance: initial value at month 0
    """
    # monthly compound rate
    monthly_rate = (1 + annual_growth_rate) ** (1 / 12) - 1

    # ensure float dtype
    df["Balance"] = df["Balance"].astype(float)

    # find first known balance in the column (if any)
    known_idx = df["Balance"].first_valid_index()
    if known_idx is None:
        raise ValueError("No known balances found — need at least one annual anchor.")

    # set month 0 to initial purchase value
    df.loc[0, "Balance"] = start_balance

    # for each known anchor, fill exponentially between previous anchor and this one
    prev_idx = 0
    prev_val = start_balance
    for idx in df.index[1:]:
        # if this row already has a known (annual) balance, update anchors
        if not np.isnan(df.loc[idx, "Balance"]):
            prev_idx = idx
            prev_val = df.loc[idx, "Balance"]
        else:
            # grow monthly from previous value
            prev_val *= (1 + monthly_rate)
            df.loc[idx, "Balance"] = prev_val

    return df



# Same as comp_int, but for annual compounding (but output interpolated to monthly amounts)
def comp_int_annual(capital, rate, years, deposits = None):
    df = comp_int_general(capital, rate, years, monthly_compound = False, deposits = deposits)
    
    # Go from one row for per year, to one row per month
    df = insert_blank_lines(df, lines_to_insert = 11, before = True)

    # Interpolate columns given that it's now one row per month ...

    df['Deposits'] = (df['Deposits'] / 12).bfill()
    df['Interest Received'] = (df['Interest Received'] / 12).bfill()

    # Fix Balance column by using a linear interpolation by adding a temporary dummary var
    df = pd.concat([pd.DataFrame(columns = df.columns, index = [0]), df])
    df = df.reset_index()

    # This fills the exponential monthly amounts (slightly more accurate than linear interpolation in last one)
    df = fill_exponential_balance(df, rate/100, capital)
    df = df[1:].reset_index()

    df['Accumulated Interest'] = df['Interest Received'].cumsum()
    return df


# Compound interest loan model to generate monthly values in a dataframe
# Can be: Monthly mortgage repayments model / p2p lending model
#
# Input parameters
# --
# CONFIGURATION
# p2p- TRUE/FALSE - whether using mortage or p2p model
# --
# LENGTH OF LOAN/INVESTMENT:
# principal - the initial size of the loan / the initial amount invested
# rate - the annual interest of the fixed rate loan as %
# years - the numer of years of the loan
# MONTHLY:
# Additional Payments - additional amounts add into loan to reduce interest and repay loan quicker
# --
# Output columns
# --
# EACH MONTH:
# payment - payment for that month (includes interest and principal as below)
# Interest Paid/Interest Received - interest paid / interest received
# Principal Paid/Capital Repaid - principal repaid / capital repaid
# Principal Remaining/Capital to be Repaid - principal/capital to be repaid/received at end of month
# Accumulated Interest - total interest paid/received end of month
def comp_int_loan(principal, rate, years, additional_payments = None, p2p = False):

    # Total monthly repayments received
    mon_rep = round(monthly_repayment(principal, rate, 12 * years), 2)

    additional_payments = additional_payments if series_has_data(additional_payments) else pd.Series([0] * years * 12)

    # Calculate first row values
    vals = {}
    vals['Interest Paid'] = int(principal * rate / 100 / 12)
    vals['Principal Paid'] = int(mon_rep - vals['Interest Paid'])
    vals['Principal Remaining'] = int(principal) - vals['Principal Paid'] - additional_payments.iloc[0]

    # Create dataframe and add first row values
    df = pd.DataFrame([vals])

    # Add all remaining (derived) rows to dataframe
    for i in range(1, years * 12):
        
        # Principal remaining at the start of the month is same as that at end of previous month
        prin_remaining_start = df.loc[i - 1, 'Principal Remaining'] 
        
        # Apply interest on principal remaining at the start of the month
        vals['Interest Paid'] = prin_remaining_start * rate / 100 / 12
        
        # Amount of principal paid in this month( monthly payment less this month's interest)
        vals['Principal Paid'] = mon_rep - vals['Interest Paid']
        
        # The amount of principal remaining at the end of this month
        vals['Principal Remaining'] = prin_remaining_start - vals['Principal Paid'] - additional_payments.iloc[i]
        df = pd.concat([df, pd.DataFrame([vals])], ignore_index=True)
    
    # Summing the total cumulative interest at end of each month
    df['Accumulated Interest'] = df['Interest Paid'].cumsum()
    
    # Add desposits column to dataframe
    df['Additional Payments'] = additional_payments
    
    # Re order columns
    df = df[['Principal Paid', 'Interest Paid', 'Additional Payments', 'Principal Remaining', 'Accumulated Interest']]
    
    # Rename columns if using rate setter model
    if p2p:
        df = df.rename(columns = {'Interest Paid':'Interest Received', 'Principal Paid':'Capital Repaid', 'Principal Remaining':'Capital to be Repaid'})
    
    return df.astype(int)