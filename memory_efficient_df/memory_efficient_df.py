import os
import pandas as pd

def df_memory(df):
    """shortcut function to view df.info(memory_usage='deep')"""
    print(df.info(memory_usage='deep'))

def optimal_dtypes(df, str_cols_exclude=None, unique_val_thresh=0.5,
                   print_to_screen=False):
    """
    Return a dict of memory-efficient dtypes for each column in df.
    
    Parameters
    ----------
    df : dataframe
    
    str_cols_exclude : list, optional
        column name(s) of dtype 'object/string' to exclude from
        the conversion of string/object to dtype 'category'

    unique_val_thresh : float, optional
        series of dtype 'object' will only be converted
        to dtype 'category' if the ratio of unique values to
        all values in series, is less than unique_val_thresh

    print_to_screen : boolean, optional
        print dict to screen

    Returns
    -------
    dictionary {Series_name: Series_dtype....}
    """
    
    df = df.copy()
    
    # INTEGER
    int_dtypes = df.select_dtypes(include=['int64']) # subset of df
    int_downcast = int_dtypes.apply(pd.to_numeric, downcast='unsigned')
    df.loc[:, [col for col in int_downcast.columns]] = int_downcast

    # FLOATS
    float_dtypes = df.select_dtypes(include=['float'])
    float_downcast = float_dtypes.apply(pd.to_numeric, downcast='float')
    df.loc[:, [col for col in float_downcast.columns]] = float_downcast

    # OBJECTS
    obj_dtypes = df.select_dtypes(include=['object'])
    
    if str_cols_exclude is not None:
        obj_dtypes.drop([col for col in str_cols_exclude],
                        axis=1, inplace=True)
        
    for col in obj_dtypes.columns:
        unique_values = len(obj_dtypes[col].unique())
        all_values = len(obj_dtypes[col])
        if unique_values / all_values < unique_val_thresh:
            df.loc[:, col] = obj_dtypes[col].astype('category')
        else:
            df.loc[:, col] = obj_dtypes[col]

    if print_to_screen:
        for key, value in column_types.items():
            print("'" + key + "'" + ": " + "'" + value + "'" + ",")
    print('\n')

    # DICTIONARY OF {COL_NAME: DTYPES}
    # list comprehension accesses .name attribute for NumPy dtype class
    return {
        col_name: col_dtype
            for col_name, col_dtype in zip(
                df.dtypes.index, [dtype.name for dtype in df.dtypes.values] 
                )
            }
