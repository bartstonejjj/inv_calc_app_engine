import pandas as pd
import itertools
from investment_models.inv_totals import add_ROI, inv_summary
from investment_models.comp_int import comp_int

def savings_acc(capital, rate, years, add_asset_cols = True, name = 'Savings Account'):
	df = comp_int(capital = capital, rate = rate, years = years)

	# Add savings account label to said columns
	df.columns = pd.MultiIndex.from_product([[name], list(df.columns)])

	df = df.astype(int)

	df = add_ROI(df, capital, df[name, 'Balance'], add_asset_cols = add_asset_cols)

	return df

def run(capital, rate, years, add_asset_cols = True, name = 'Savings Account'):

	df = savings_acc(capital, rate, years, add_asset_cols = add_asset_cols, name = name)
	return df, inv_summary(df, name) 