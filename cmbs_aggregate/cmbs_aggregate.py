from datetime import datetime
import pandas as pd
import numpy as np
import shutil
import glob
import os


main_dir = r'C:\Users\storres.759NYY1\Desktop\cmbu\test1'


def lead_convert(main_folder=main_dir, lead_pattern='Morningstar*',
                lead_csv='combined.csv'):
    
    """
    Convert .html files into one .csv file.

    Parameters
    ----------
    main_folder : string
        Directory containing Lead Generator Files
    lead_pattern : string, default 'Morningstar*'
        File name pattern to match
    lead_csv : string, default 'combined (date).csv'
        Optional file name for CSV file.

    Returns
    -------
    None
    
    Notes
    -----
    * Function should be run in directory containing
      only the files you need (i.e. lead generator & 
      data export files).
    * Lead Generator files will have .xls extension but
      are actually .html file format.
    * lead_csv argument can have a '.csv' extension
      or be left blank. 'combined.csv' == 'combined'.
    * lead_pattern matches file names that start with
      argument provided.
    """

    os.chdir(main_folder)

    lead_folders = [
        'lead_html_files', 
        'lead_csv_files',
        'lead_combined' 
        ]

    [os.mkdir(folder) for folder in lead_folders]

    lead_abs_paths = glob.glob(os.path.join(main_folder, lead_pattern))

    lead_basenames = [file.split('\\')[-1] for file in lead_abs_paths]

    # Read in HTML files, save as CSV. HTML files are moved to HTML folder.
    for first_file in lead_basenames:
        first_df = pd.read_html(first_file, header=0)
        first_df[0].to_csv(os.path.join(lead_folders[1],
                                        first_file.strip('.xls')
                                        + '.csv'), index=False)

        shutil.move(main_folder
                    + '\\'
                    + first_file,
                    lead_folders[0])

    all_csv_files = glob.glob(os.path.join(lead_folders[1], lead_pattern))
    all_dfs = []

    # Read in CSV files, append to list and concatenate.
    for file in all_csv_files:
        each_df = pd.read_csv(file, encoding='ISO-8859-1')
        all_dfs.append(each_df)

    cmbs = pd.concat(all_dfs, axis=0, ignore_index=True)

    os.chdir(lead_folders[2])
    
    date_today = datetime.today().strftime('%Y-%m-%d')
    final_csv_name = lead_csv.split('.')[0] + ' ' + date_today + '.csv'
    cmbs.to_csv(final_csv_name, index=False)

    "Lead Generator (Combined CSV) path: {}".format(
        os.path.join(main_folder, lead_folders[2], lead_csv))

    return None


def datax_convert(main_folder=main_dir, datax_pattern='*.xls',
                ignore_if_starts_with='Morningstar'):
    
    """
    Convert .txt files into .csv files.

    Parameters
    ----------
    main_folder : string
        Directory containing Data Export Files
    datax_pattern : string, default '*.xls'
        File extension pattern to match
    ignore_if_starts_with : string, default 'Morningstar'
        Ignore file names that start with argument

    Returns
    -------
    None
    

    Notes
    -----
    * Function should be run in directory containing
      only the files you need (i.e. Lead Generator & 
      Data Export files).
    * Data Export files will have .xls extension but
      are actually .txt file format.
    * Column name "Prospectus ID" will be modified
      for consistency with Lead Generator column
      "Pros ID". "Deal ID" & "Pros ID" are the two
      key columns that must be used to merge any
      Lead Generator or Data Export files on.
    * csv files will be named according to their
      original file name.
    """

    os.chdir(main_folder)

    datax_folders = [
        'datax_txt_files',
        'datax_csv_files'
        ]

    [os.mkdir(folder) for folder in datax_folders]

    dfs = {}

    # List of files that satisfy datax_pattern & ignore_if_starts_with
    datax_abs_paths = [
        file for file in glob.glob(os.path.join(main_folder, datax_pattern))
        if not os.path.basename(file).startswith(ignore_if_starts_with)
        ]
    
    datax_basenames = [item.lower().split('\\')[-1] for item in datax_abs_paths]
    basenames_no_extensions = [file[:-4] for file in datax_basenames]

    # 'error_bad_lines=False' is necessary to read the 'Morningstar Loan' file.
    for name, filename in zip(basenames_no_extensions, datax_basenames):
        dfs[name] = pd.read_table(filename, error_bad_lines=False)

    for key in dfs.keys():
        dfs[key]['Loan Prospectus ID'].replace("'","",regex=True,
                                               inplace=True)
        dfs[key].rename(columns={'Loan Prospectus ID': 'Pros ID'},
                        inplace=True)

    for file in datax_basenames:
        shutil.move(main_folder + '\\' + file, datax_folders[0])

    os.chdir(datax_folders[1])

    date_today = datetime.today().strftime('%Y-%m-%d')

    for name in dfs.keys():
        dfs[name].to_csv(str(name) + ' ' + date_today + '.csv', index=False)

    "Support Files path: {}".format(
        os.path.join(main_folder, datax_folders[1]))

    return None
