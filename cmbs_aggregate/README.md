# cmbs_aggregate
## About
These two automation functions were created to help with a tedious, time-consuming task.

Since CMBS data is updated and published monthly, each month I was downloading countless data files that needed to be manually combined into one file and saved in a usable format.  The majority of the files are HTML files, while others are text (tab delimited) files. I wanted to create one or two functions that would load in each file, by name, convert them to a CSV file and join the files that needed to be joined.

The first functions loads all the HTML files, converts them to CSV and joins the CSV files into one file. Each group of files are moved to their respective folders that the function created (i.e. html files are moved to the html file folder, the concatenated csv file is moved to its csv folder).

Similarly, the text files are loaded, a column is modified for consistency across all files, and saved as csv files.
