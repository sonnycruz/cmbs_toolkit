import pandas as pd
import numpy as np
import shutil
import glob
import os


# main_dir_w_files: The main directory must contain only the files
# needed and they must all have default values.

main_dir_w_files = r'C:\Users\storres.759NYY1\Desktop\cmbu'
os.chdir(main_dir_w_files)


def agg_all(lead_pattern='Morningstar*', lead_csv='combined.csv',
            support_pattern='*.xls', lead_generator=True,
            sup_files=True, merge_files=True,
            all_in_one_folder=True):
    
    """
    lead_pattern='Morningstar*', lead_csv='combined.csv',
    sup_pattern='*.xls'
    """
    
    start_path = os.getcwd()
    
    if lead_generator:
        
        folder_names = [
            '0.lead_html_files', # original lead generator files
            '1.lead_csv_files', # lead gen files converted to csv
            '2.lead_combined' # all csv concatenated into one file
            ] 
        
        [os.mkdir(fn) for fn in folder_names]

                        
        # Get the full paths of each file that matches the lead_pattern
        # (Lead Generator files will start with "Morningstar")
        stnd_file_paths = glob.glob(os.path.join(start_path, lead_pattern))
        
        # Isolate file name (with extension) in each path.
        # You can also use [os.path.basename(file) for file in stnd_file_paths]
        stnd_names = [file.split('\\')[-1] for file in stnd_file_paths]

        # Read in each file (in this case they are html files despite having a
        # .xls extension) that have names that
        # meet the lead_pattern criteria. Each will then be saved as csv files.
        for first_file in stnd_names:
            first_df = pd.read_html(first_file, header=0)
            first_df[0].to_csv(os.path.join(folder_names[1],
                                            first_file.strip('.xls')
                                            + '.csv'), index=False)
            # Original HTML files are moved to HTML folder.
            shutil.move(start_path
                        + '\\'
                        + first_file,
                        folder_names[0])

        # all_files is a list of paths that are just extensions of the
        # current path (start_path). start_path\1.lead_csv_files\Morningstar*
        all_files = glob.glob(os.path.join(folder_names[1], lead_pattern))
        all_dfs = []

        for file in all_files:
            each_df = pd.read_csv(file, encoding='ISO-8859-1')
            all_dfs.append(each_df)

        cmbs = pd.concat(all_dfs, axis=0, ignore_index=True)

        # Finally, concatenated Lead Generator file is saved as a csv file.
        os.chdir(folder_names[2])
        cmbs.to_csv(lead_csv, index=False)

        "Lead Generator (CMBS Universe) path: {}".format(
            os.path.join(start_path, folder_names[2], lead_csv))

    # Similar tasks will be completed on the support files (IRP Property,
    # IRP Loan, Morningstar Loan)

    if support_pattern:
        
        os.chdir(start_path)
        
        support_folders = [
            '3.sup_txt_files', # original support files
            '4.sup_csv_files' # support files converted to csv
            ]
        [os.mkdir(fn) for fn in support_folders]
        [folder_names.append(folder) for folder in support_folders]

        dfs = {}
        sup_file_paths = glob.glob(os.path.join(start_path, support_pattern)) # full path name
        sup_names = [item.lower().split('\\')[-1] for item in sup_file_paths] # list of file names
        var_names = [file[:-4] for file in sup_names] # name of the file (no extension)
        
        for var, file in zip(var_names, sup_names):
            dfs[var] = pd.read_table(file, error_bad_lines=False)

        # these small changes make joining the various files much easier.
        for key in dfs.keys():
            dfs[key]['Loan Prospectus ID'].replace("'","",regex=True,
                                                 inplace=True)
            dfs[key].rename(columns={'Loan Prospectus ID': 'Pros ID'},
                            inplace=True)

        for file in sup_names:
            shutil.move(start_path + '\\' + file, folder_names[3])

        os.chdir(folder_names[4])

        for name in dfs.keys():
            dfs[name].to_csv(str(name) + '.csv', index=False)

        "Support Files path: {}".format(
            os.path.join(start_path, folder_names[4]))

    if merge_files: #Columns Deal ID and Pros ID must be objects(strings) to avoid categorical dtype merge issues???
        
        os.chdir(start_path)
        merge_folder = '5.all_merged' # lead gen and support files merged
        os.mkdir(merge_folder)
        folder_names.append(merge_folder)

        merge_cols = ['Deal ID', 'Pros ID']
        cmbsu_dtype = {'Priority': 'uint8', 'Tape Date': 'category', 'Run Date': 'category', 'Unnamed: 3': 'float32', 'Servicer Loan ID': 'category', 'Loan Name': 'object', 'Address': 'object', 'City': 'category', 'State': 'category', 'Zip': 'category', 'MSA': 'category', 'Region': 'category', 'Orig. Loan Balance': 'category', 'Cut-off Loan Balance': 'object', 'Current Loan Balance': 'object', 'P&I Advances': 'category', 'T&I Advances': 'category', 'Other Advances Paid': 'category', 'Cumulative ASER': 'category', 'Accrued Unpaid Adv Int': 'category', 'Total Loan Exposure': 'object', 'Unnamed: 23': 'float32', 'Property Type': 'category', 'Property Sub-Type': 'category', '# of Props': 'uint16', 'Gross Coupon': 'float32', 'Net Coupon': 'float32', 'Unnamed: 29': 'float32', 'Rate Type': 'category', 'Orig. Terms to Maturity (months)': 'uint16', 'Current Terms to Maturity (months)': 'uint16', 'Orig. Amort Terms': 'uint16', 'Current Amort Terms': 'int64', 'Orig. IO Terms': 'float32', 'Current IO Terms': 'float32', 'Seasoning': 'uint16', 'Origination Date': 'category', 'Unnamed: 39': 'float32', 'Securitization Year': 'uint16', 'Maturity Date / ARD': 'category', 'Unnamed: 42': 'float32', 'Prin. Pmt.': 'category', 'Int. Pmt.': 'category', 'Unnamed: 45': 'float32', 'Modification Desc.': 'category', 'Modification Date': 'category', 'Unnamed: 48': 'float32', 'Originator': 'category', 'Master Servicer': 'category', 'Special Servicer': 'category', 'Trustee': 'category', 'Borrower Name': 'category', 'Borrower Address': 'category', 'Borrower City': 'category', 'Borrower State': 'category', 'Borrower Zip': 'category', 'Borrower Contact': 'category', 'Borrower Phone #': 'category', 'County Website': 'category', 'Unnamed: 61': 'float32', 'Appraised Value': 'category', 'Unnamed: 63': 'float32', 'Appraised Date': 'category', 'Sq. Ft.': 'float32', 'Units': 'float32', 'Unnamed: 67': 'float32', 'Year Built': 'float32', 'Year Renovated': 'float32', 'Financial Stmt. Date': 'category', 'Revenue Amt.': 'category', 'Expense Amt.': 'category', 'NOI': 'float32', 'NCF': 'float32', 'Debt Yield': 'category', 'DSCR': 'float32', 'Occupancy Rate (%)': 'float32', 'Current LTV': 'float32', 'Original LTV': 'float32', 'Unnamed: 80': 'float32', 'Lockout': 'uint8', 'Defeasance': 'uint8', 'Yield Maint.': 'uint16', 'Prepay Prem': 'uint16', 'Open': 'int64', 'Unnamed: 86': 'float32', 'Current Call Protection Status': 'category', 'Defeasance Cost': 'float32', 'Prepay Prem Amt.': 'object', 'Prepay Prem % of UPB': 'float32', 'Mstar Cap Rate': 'float32', 'Cap Rate Used for Prop Value': 'float32', 'Estimated Property Value': 'category', 'Estimated LTV': 'float32', 'Payoff Amount': 'float32', 'Refinancing Proceeds': 'object', 'Refinancing Proceeds % of UPB': 'category', 'Unnamed: 98': 'float32', 'Loan Status': 'category', 'Special Serviced Ind': 'category', 'MR SS Xfer Date': 'category', 'Unnamed: 102': 'float32', 'Watchlist Ind': 'category', 'Servicer Watchlist Date': 'category', 'WL Codes': 'category', 'Bankruptcy Ind': 'category', 'B-Piece Buyer': 'category', 'Links': 'float32'}
        loan_dtype = {'Tape Date': 'category', 'Servicer Loan ID': 'object', 'Servicer Prospectus Loan ID': 'object', 'Distribution Date': 'category', 'Update Date': 'category', 'Asset Name': 'object', 'City': 'category', 'State': 'category', 'ZIP': 'category', 'Current Balance Amount': 'float32', 'Maturity Date': 'category', 'Maturity Months': 'float32', 'Asset Type': 'category', 'Property Subtype': 'category', 'Most Recent Start Date': 'category', 'Most Recent End Date': 'category', 'Most Recent Number of Months': 'float32', 'Most Recent Revenue': 'float32', 'Most Recent Expense': 'float32', 'Most Recent NOI': 'float32', 'Most Recent NCF': 'float32', 'Most Recent NOI DSCR': 'float32', 'Most Recent NCF DSCR': 'float32', 'Most Recent Occupancy Rate': 'float32', 'Most Recent Appraisal Date': 'category', 'Most Recent Appraised Value': 'float32', 'Most Recent Assumption Date': 'category', 'Most Recent Modification': 'category', 'Most Recent Modification Date': 'category', 'Modified Payment Rate': 'float32', 'Modified Rate': 'float32', 'Special Serviced Indicator': 'category', 'Special Servicer': 'category', 'Amortization Type': 'category', 'Hyper Amortization Date': 'category', 'I/O End Date': 'category', 'Workout Code': 'category', 'Workout Fee Amount': 'float32', 'Date Added To Watchlist': 'category', 'Resolution Date': 'category', 'Foreclosure Date': 'category', 'REO Date': 'category', 'Call Protection Summary': 'category', 'Loan Paid To Date': 'category', 'Loan Status Type': 'category', 'Paid Off Date': 'category', 'Appraisal Reduction Amount': 'float32', 'Appraisal Reduction Date': 'category', 'Liquidation Code': 'category', 'Liquidation Expense': 'float32', 'Liquidation Fee Amount': 'float32', 'Net Proceeds Received  on Liquidation ': 'float32', 'Realized Loss': 'float32', 'Servicer Transation ID': 'category', 'Balloon Indicator': 'category', 'Bloomberg Deal ID': 'category', 'Crossed Loan ID': 'category', 'Cumulative ASER': 'float32', 'Most Recent ASER': 'float32', 'Defeasance': 'float32', 'Defeasance Status': 'category', 'Prepayment Penalty': 'float32', 'Prepayment Penalty Amount': 'float32', 'Cumulative Accrued Unpaid Advance Interest': 'float32', 'Other Advances': 'float32', 'Other Principal Adjustments': 'float32', 'P&I Advances': 'float32', 'Reimbursed Interest On Advances': 'float32', 'Special Servicing Fee Amount Plus Adjustments': 'float32', 'T&I Advances': 'float32', 'Previous Year Start Date': 'float32', 'Previous Year End Date': 'category', 'Previous Year Number of Months': 'float32', 'Previous Year Revenue': 'float32', 'Previous Year Expense': 'float32', 'Previous Year NOI': 'float32', 'Previous Year NCF': 'float32', 'Previous Year NOI DSCR': 'float32', 'Previous Year NCF DSCR': 'float32', 'Previous Year Occupancy Rate': 'float32', 'Second Previous Year Start Date': 'float32', 'Second Previous Year End Date': 'category', 'Second Previous Year Number of Months': 'float32', 'Second Previous Year Revenue': 'float32', 'Second Previous Year Expense': 'float32', 'Second Previous Year NOI': 'float32', 'Second Previous Year NCF': 'float32', 'Second Previous Year NOI DSCR': 'float32', 'Second Previous Year NCF DSCR': 'float32', 'Second Previous Year Occupancy Rate': 'float32', 'Issuance Start Date': 'float32', 'Issuance End Date': 'category', 'Issuance Number of Months': 'float32', 'Issuance Revenue': 'float32', 'Issuance Expense': 'float32', 'Issuance NOI': 'float32', 'Issuance NCF': 'float32', 'Issuance NOI DSCR': 'float32', 'Issuance NCF DSCR': 'float32', 'Issuance Occupancy Rate': 'float32', 'Yield Maintenance': 'float32', 'Underwriter': 'category', 'Underwritten DSCR': 'float32', 'Underwritten NOI': 'float32', 'Number Of Properties': 'uint16', 'Most Recent Debt Service': 'float32', 'Most Recent Return Date': 'category', 'Most Recent Transfer Date': 'category', 'MSA': 'category', 'Loan Origination Date': 'category', 'Property Square Feet': 'float32', 'Current Balance per Square Foot': 'float32', 'Bankruptcy Date': 'category', 'Bankruptcy Indicator': 'category', 'Number Of Installments Paid': 'float32', 'Number Of Remaining Installments': 'int64', 'Deal Type': 'category', 'Original Loan Amount': 'float32', 'Original LTV': 'float32', 'Master Servicer ': 'category', 'NOI': 'float32', 'Occupancy Rate': 'float32', 'Original Amortization Term Months': 'uint16', 'Original Interest Only Term': 'float32', 'Debt Yield': 'float32', 'DSCR': 'float32', 'DSCR At Cutoff': 'float32', 'Loan Originator': 'category', 'Remaining Interest Only Term': 'float32', 'Units': 'float32', 'Coupon': 'float32', 'Borrower Name': 'category', 'Trepp Loan ID': 'category', 'Securitized LTV': 'float32', 'Factor': 'float32', 'Total Number Of Installments': 'uint16'}
        prop_dtype = {'Property Number': 'category', 'Tape Date': 'category', 'Servicer Loan ID': 'category', 'Servicer Prospectus Loan ID': 'category', 'Property Name': 'object', 'Property Address': 'object', 'Property Square Feet': 'float32', 'Date Lease Rollover Review': 'category', 'Percent Expiring 1-12 months': 'float32', 'Percent Expiring 13-24 months': 'float32', 'Percent Expiring 25-36 months': 'float32', 'Percent Expiring 37-48 months': 'float32', 'Largest Tenant Name': 'category', 'Largest Tenant Square Feet': 'float32', 'Largest Tenant Lease Expiration': 'category', 'Second Largest Tenant Name': 'category', 'Second Largest Tenant Square Feet': 'float32', 'Second Largest Tenant Lease Expiration': 'category', 'Third Largest Tenant Name': 'category', 'Third Largest Tenant Square Feet': 'float32', 'Third Largest Tenant Lease Expiration': 'category', 'Fourth Largest Tenant Name': 'category', 'Fourth Largest Tenant Square Feet': 'float32', 'Fourth Largest Tenant Lease Expiration': 'category', 'Fifth Largest Tenant Name': 'category', 'Fifth Largest Tenant Square Feet': 'float32', 'Fifth Largest Tenant Lease Expiration': 'category', 'Property Type': 'category', 'Current Balance': 'float32', 'State': 'category', 'Year Built': 'float32', 'Year Renovated': 'float32', 'ZIP': 'category', 'City': 'category'}
        ms_dtype = {'Data As of Date': 'category', 'Deal View Data As of Date': 'category', 'DealView Date': 'category', 'Update Date': 'category', 'Servicer Loan ID': 'object', 'Asset Name': 'object', 'Probability of Default': 'float32', 'Forecasted Loss': 'float32', 'Morningstar Estimated Value': 'float32', 'Valuation Deficiency ': 'float32', 'Valuation Method ': 'category', 'Valuation Date': 'category', 'Morningstar Top 10 Comment': 'category', 'Morningstar Watchlist Comment': 'category', 'Morningstar Watchlist Indicator': 'category', 'Loan Percent Of Deal': 'float32'}

        
        cmbsu = pd.read_csv(os.path.join(folder_names[2], lead_csv), dtype=cmbsu_dtype)
        loan = pd.read_csv(glob.glob(os.path.join(folder_names[4], 'l*'))[0], dtype=loan_dtype) #"[0]" is necessary to access the string inside of the list that glob.glob returns
        prop = pd.read_csv(glob.glob(os.path.join(folder_names[4], 'o*'))[0], dtype=prop_dtype)
        ms = pd.read_csv(glob.glob(os.path.join(folder_names[4], 'm*'))[0], dtype=ms_dtype)

    
        loan_prop = pd.merge(loan, prop, how='left', on=merge_cols)
        cmbsu_loan_ms = pd.merge(pd.merge(cmbsu, loan, how='left', on=merge_cols), ms, how='left', on=merge_cols)

        
        os.chdir(folder_names[5])
        loan_prop.to_csv('loan_prop.csv', index=False)
        cmbsu_loan_ms.to_csv('cmbsu_loan_ms.csv', index=False)
