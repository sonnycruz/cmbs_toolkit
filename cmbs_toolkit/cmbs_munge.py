import os
import pandas as pd
import numpy as np

def load_cmbs(file, main_folder=cmbs_u_dir, dtype=None, converters=None):
    """Load CSV file as DataFrame."""
    csv_path = os.path.join(main_folder, file)
    return pd.read_csv(csv_path, encoding="ISO-8859-1",
                       dtype=dtype, converters=converters)

def date_convert(df, col):
    """Convert col in df to datetime format."""
    df[col] = pd.to_datetime(df[col], infer_datetime_format=True)

def year_col(df, col, year_col):
    """
    Create a year column for a given datetime column.

    df: DataFrame
    col : str
        datetime column to derive year values from
    year_col : str
        Column name for the newly created year column
    """
    df[year_col] = df[col].dt.year

def currency(df, col):
    """Modify column, in place, w/ currency values to float values."""
    df[col] = df[col].str.replace("[$(),]","").fillna(0).astype(float)

def drop_cols(df, col_arg, by_word=False):
    """
    Drop col if col_arg is present in col name.
        
    Parameters
    ----------
    df : dataframe
    col_arg : str
        Can be word in col names to drop or literal column name
    word : boolean, default False
        True if col_arg is keyword in columns to be dropped
        False if col_arg is column name
        
    Returns
    -------
    None
    
    Examples
    -------
    >> drop_cols(my_df, col_arg='junk_col')
    
    >> drop_cols(my_df, col_arg='junk word', word=True)
    """
    if by_word:
        df.drop(columns=[col for col in df.columns if col_arg in col],
                inplace=True)
    else:
        df.drop(col_arg, axis=1, inplace=True)
