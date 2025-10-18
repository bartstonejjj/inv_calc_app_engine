import pandas as pd

# Add a month index starting at 1, labelled Month
def month_index(df):
    df = df.reset_index(drop = False)
    df['index'] = df['index'] + 1
    df = df.rename(columns = {'index':'Month'})
    return df.set_index('Month')

# Format investment model dataframe to make it easier to the eye for users
def pretty_model(df):
    df = df.dropna(how = 'all', axis = 1)
    df = df.fillna('')
    return month_index(df)