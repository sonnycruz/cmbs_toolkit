import pandas as pd
import numpy as np
import shutil
import glob
import os


main_dir = r'C:\Users\storres.759NYY1\Desktop\cmbu\test1'


def lead_convert(main_folder=main_dir, lead_pattern='Morningstar*',
                lead_csv='combined.csv'):
    
    """
    Function reads Lead Generator HTML files that match 'lead_pattern',
    converts the files to CSV and then concatenates the CSV files,
    along the first axis, into a single file. All files are organized
    into newly created directories. NOTE: Morningstar.xls files are of
    the file format .html, despite the .xls extension.
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

    # Read in HTML files, save as CSV & HTML files will be moved to HTML folder.
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
    cmbs.to_csv(lead_csv, index=False)

    "Lead Generator (Combined CSV) path: {}".format(
        os.path.join(main_folder, lead_folders[2], lead_csv))


def datax_convert(main_folder=main_dir, datax_pattern='*.xls',
                ignore_if_starts_with='Morningstar'):
    
    """
    Function accepts Data Export (or 'datax') files such as
    IRP Loan.xls, IRP Property.xls or IRP Deal.xls and converts
    the files to CSV. The Pros ID column is slightly modified to
    prepare files for merging files later, if desired. All files
    are organized into newly created directories.
    NOTE: Data Export files are of the file format '.txt',
    despite the '.xls' extensions.
    """

    os.chdir(main_folder)

    datax_folders = [
        'datax_txt_files',
        'datax_csv_files'
        ]

    [os.mkdir(folder) for folder in datax_folders]

    dfs = {}

    # List of files that both meet 'datax_pattern' criteria and ignore
    # file names according to 'ignore_if_starts_with'
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

    for name in dfs.keys():
        dfs[name].to_csv(str(name) + '.csv', index=False)

    "Support Files path: {}".format(
        os.path.join(main_folder, datax_folders[1]))
