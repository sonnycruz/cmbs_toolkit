# memory_efficient_df

Significantly reduce your dataframe's memory usuage! 

The main function (optimal_dtypes contained in memory_efficient_df.py) was created to optimize memory usuage when working with large files. When you pass a Pandas DataFrame object to the function, the function will create a dictionary of memory-efficient datatypes that can be used when loading the same dataframe in the future. You will find that, given the amount of memory required for string objects, the conversion to the datatype 'category' will yield the most benefits.

The folder /my_cmbs_dtypes contains my preferred data types for each dataframe I typically use.

## Example

>> dtypes_dict = optimal_dtypes(my_df)


>> efficient_df = pd.read_csv('df_file.csv', dtype=dtypes_dict)

## More Information
The function was created by modifying bits of code available in a blogpost posted by dataquest.io and with dataquest.io's permission. 

dataquest page: https://www.dataquest.io/blog/pandas-big-data/
