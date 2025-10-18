import pandas as pd

# Return true if series exists and has data
def series_has_data(s):
    if s is None:
        return False
    elif type(s) == pd.core.series.Series:
        return True if len(s) > 0 else False
    else:
        return False

def series_from_index(df_or_series):
    return pd.Series(df_or_series.index, index = df_or_series.index)

# Iterate over each row by yielding each row a (sub) dataframe
def df_row_iter(df):
    for i in range(len(df)):
        yield df.loc[[i]]

# Create a blank dataframe of size: length x len(columns), with columns has columns
def blank_df(columns, length):
    return pd.DataFrame(columns = columns, index = list(range(length)))

# Insert 'lines_to_insert' lines between every line in DataFrame (either before or after)
def insert_blank_lines(df, lines_to_insert, before = True):
    dfs = []
    for row_df in df_row_iter(df):
        if before:
            dfs.append(blank_df(df.columns, lines_to_insert))
        
        dfs.append(row_df)
        
        if not before:
            dfs.append(blank_df(df.columns, lines_to_insert))
    return pd.concat(dfs).reset_index(drop = True)