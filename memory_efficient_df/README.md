# memory_efficient_df

Significantly reduce your dataframe's memory usuage! 

The main function (optimal_dtypes contained in memory_efficient_df.py) was created to optimize memory usuage when working with large files. When you pass a Pandas DataFrame object to the function, the function will create a dictionary of memory-efficient datatypes that can be used when loading the same dataframe in the future.

## Example

>> dtypes_dict = optimal_dtypes(my_df)
...
>> efficient_df = pd.read_csv('C:\User\Desktop\Df_FileName', dtype=dtypes_dict)

The function was created by modifying bits of code available in a blogpost posted by dataquest.io and with dataquest.io's permission. 

dataquest page: https://www.dataquest.io/blog/pandas-big-data/
