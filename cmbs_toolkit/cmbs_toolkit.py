import os
import pandas as pd
import numpy as np
from functools import partial
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from mpl_toolkits.basemap import Basemap
pd.set_option('display.float_format', lambda x: '%.2f' % x)


cmbs_u_dir = r'C:\Users\storres.759NYY1\Desktop\cmbu\6. all'
cmbs_u = 'combined.csv'

sup_main_dir = r'C:\Users\storres.759NYY1\Desktop\cmbu\6. all'
irp_loan = 'loan template 5.24.2017.csv'
irp_prop = 'occ 8.24.2017.csv'

listings_dir = r'C:\Users\storres.759NYY1\Desktop\Legacy Maturities & Universe\19. May 2018\May Assumptions\0. Data\Set 2'
listings_file = 'New_update_new.csv'

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


# LEAD GENERATOR FILE
cmbsu_dtype_practical = {'Priority': 'uint8', 'Tape Date': 'category', 'Run Date': 'category', 'Unnamed: 3': 'float32', 'Deal ID': 'object', 'Pros ID': 'object', 'Servicer Loan ID': 'category', 'Loan Name': 'object', 'Address': 'object', 'City': 'category', 'State': 'category', 'Zip': 'category', 'MSA': 'category', 'Region': 'category', 'Orig. Loan Balance': 'category', 'Cut-off Loan Balance': 'object', 'Current Loan Balance': 'object', 'P&I Advances': 'category', 'T&I Advances': 'category', 'Other Advances Paid': 'category', 'Cumulative ASER': 'category', 'Accrued Unpaid Adv Int': 'category', 'Total Loan Exposure': 'object', 'Unnamed: 23': 'float32', 'Property Type': 'category', 'Property Sub-Type': 'category', '# of Props': 'uint16', 'Gross Coupon': 'float32', 'Net Coupon': 'float32', 'Unnamed: 29': 'float32', 'Rate Type': 'category', 'Orig. Terms to Maturity (months)': 'uint16', 'Current Terms to Maturity (months)': 'uint16', 'Orig. Amort Terms': 'uint16', 'Current Amort Terms': 'int64', 'Orig. IO Terms': 'float32', 'Current IO Terms': 'float32', 'Seasoning': 'uint16', 'Origination Date': 'object', 'Unnamed: 39': 'float32', 'Securitization Year': 'uint16', 'Maturity Date / ARD': 'object', 'Unnamed: 42': 'float32', 'Prin. Pmt.': 'category', 'Int. Pmt.': 'category', 'Unnamed: 45': 'float32', 'Modification Desc.': 'category', 'Modification Date': 'object', 'Unnamed: 48': 'float32', 'Originator': 'category', 'Master Servicer': 'category', 'Special Servicer': 'category', 'Trustee': 'category', 'Borrower Name': 'category', 'Borrower Address': 'category', 'Borrower City': 'category', 'Borrower State': 'category', 'Borrower Zip': 'category', 'Borrower Contact': 'category', 'Borrower Phone #': 'category', 'County Website': 'category', 'Unnamed: 61': 'float32', 'Appraised Value': 'object', 'Unnamed: 63': 'float32', 'Appraised Date': 'object', 'Sq. Ft.': 'float32', 'Units': 'float32', 'Unnamed: 67': 'float32', 'Year Built': 'float32', 'Year Renovated': 'float32', 'Financial Stmt. Date': 'object', 'Revenue Amt.': 'object', 'Expense Amt.': 'object', 'NOI': 'float32', 'NCF': 'float32', 'Debt Yield': 'category', 'DSCR': 'float32', 'Occupancy Rate (%)': 'float32', 'Current LTV': 'float32', 'Original LTV': 'float32', 'Unnamed: 80': 'float32', 'Lockout': 'uint8', 'Defeasance': 'uint8', 'Yield Maint.': 'uint16', 'Prepay Prem': 'uint16', 'Open': 'int64', 'Unnamed: 86': 'float32', 'Current Call Protection Status': 'category', 'Defeasance Cost': 'float32', 'Prepay Prem Amt.': 'object', 'Prepay Prem % of UPB': 'float32', 'Mstar Cap Rate': 'float32', 'Cap Rate Used for Prop Value': 'float32', 'Estimated Property Value': 'object', 'Estimated LTV': 'float32', 'Payoff Amount': 'float32', 'Refinancing Proceeds': 'object', 'Refinancing Proceeds % of UPB': 'object', 'Unnamed: 98': 'float32', 'Loan Status': 'category', 'Special Serviced Ind': 'category', 'MR SS Xfer Date': 'object', 'Unnamed: 102': 'float32', 'Watchlist Ind': 'category', 'Servicer Watchlist Date': 'object', 'WL Codes': 'category', 'Bankruptcy Ind': 'category', 'B-Piece Buyer': 'category', 'Links': 'float32'}
cmbs = load_cmbs(file=cmbs_u, main_folder=cmbs_u_dir, dtype=cmbsu_dtype_practical)

cmbs_dates = ['MR SS Xfer Date', 'Maturity Date / ARD', 'Origination Date']

for date in cmbs_dates:
	date_convert(cmbs, date)    

# Convert column into usable integer dtype
cm_money = partial(currency, cmbs)
cm_money('Current Loan Balance')

# Create a categorical column for UPB ranges:
loan_bins = [0, 2, 3, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 1000, 2000]
cmbs['upb_cat_mm'] = pd.cut(cmbs['Current Loan Balance'] / 1000000, loan_bins)


# IRP LOAN DF
loan_dtype_practical = {'Deal ID': 'object', 'Pros ID': 'object', 'Tape Date': 'category', 'Servicer Loan ID': 'object', 'Servicer Prospectus Loan ID': 'object', 'Asset Name': 'object', 'City': 'category', 'State': 'category', 'ZIP': 'category', 'Current Balance Amount': 'float32', 'Maturity Date': 'category', 'Maturity Months': 'float32', 'Asset Type': 'category', 'Property Subtype': 'category', 'Most Recent Start Date': 'category', 'Most Recent End Date': 'object', 'Most Recent Number of Months': 'float32', 'Most Recent Revenue': 'float32', 'Most Recent Expense': 'float32', 'Most Recent NOI': 'float32', 'Most Recent NCF': 'float32', 'Most Recent NOI DSCR': 'float32', 'Most Recent NCF DSCR': 'float32', 'Most Recent Occupancy Rate': 'float32', 'Most Recent Appraisal Date': 'object', 'Most Recent Appraised Value': 'float32', 'Most Recent Assumption Date': 'object', 'Most Recent Modification': 'category', 'Most Recent Modification Date': 'object', 'Modified Payment Rate': 'float32', 'Modified Rate': 'float32', 'Special Serviced Indicator': 'category', 'Special Servicer': 'category', 'Amortization Type': 'category', 'Hyper Amortization Date': 'category', 'I/O End Date': 'category', 'Workout Code': 'category', 'Workout Fee Amount': 'float32', 'Date Added To Watchlist': 'object', 'Resolution Date': 'category', 'Foreclosure Date': 'category', 'REO Date': 'category', 'Call Protection Summary': 'category', 'Loan Paid To Date': 'object', 'Loan Status Type': 'category', 'Paid Off Date': 'object', 'Appraisal Reduction Amount': 'float32', 'Appraisal Reduction Date': 'category', 'Liquidation Code': 'category', 'Liquidation Expense': 'float32', 'Liquidation Fee Amount': 'float32', 'Net Proceeds Received  on Liquidation ': 'float32', 'Realized Loss': 'float32', 'Servicer Transation ID': 'category', 'Balloon Indicator': 'category', 'Bloomberg Deal ID': 'category', 'Crossed Loan ID': 'category', 'Cumulative ASER': 'float32', 'Most Recent ASER': 'float32', 'Defeasance': 'float32', 'Defeasance Status': 'category', 'Prepayment Penalty': 'float32', 'Prepayment Penalty Amount': 'float32', 'Cumulative Accrued Unpaid Advance Interest': 'float32', 'Other Advances': 'float32', 'Other Principal Adjustments': 'float32', 'P&I Advances': 'float32', 'Reimbursed Interest On Advances': 'float32', 'Special Servicing Fee Amount Plus Adjustments': 'float32', 'T&I Advances': 'float32', 'Previous Year Start Date': 'float32', 'Previous Year End Date': 'object', 'Previous Year Number of Months': 'float32', 'Previous Year Revenue': 'float32', 'Previous Year Expense': 'float32', 'Previous Year NOI': 'float32', 'Previous Year NCF': 'float32', 'Previous Year NOI DSCR': 'float32', 'Previous Year NCF DSCR': 'float32', 'Previous Year Occupancy Rate': 'float32', 'Second Previous Year Start Date': 'float32', 'Second Previous Year End Date': 'object', 'Second Previous Year Number of Months': 'float32', 'Second Previous Year Revenue': 'float32', 'Second Previous Year Expense': 'float32', 'Second Previous Year NOI': 'float32', 'Second Previous Year NCF': 'float32', 'Second Previous Year NOI DSCR': 'float32', 'Second Previous Year NCF DSCR': 'float32', 'Second Previous Year Occupancy Rate': 'float32', 'Issuance Start Date': 'float32', 'Issuance End Date': 'object', 'Issuance Number of Months': 'float32', 'Issuance Revenue': 'float32', 'Issuance Expense': 'float32', 'Issuance NOI': 'float32', 'Issuance NCF': 'float32', 'Issuance NOI DSCR': 'float32', 'Issuance NCF DSCR': 'float32', 'Issuance Occupancy Rate': 'float32', 'Yield Maintenance': 'float32', 'Underwriter': 'category', 'Underwritten DSCR': 'float32', 'Underwritten NOI': 'float32', 'Number Of Properties': 'uint16', 'Most Recent Debt Service': 'float32', 'Most Recent Return Date': 'category', 'Most Recent Transfer Date': 'object', 'MSA': 'category', 'Loan Origination Date': 'object', 'Property Square Feet': 'float32', 'Current Balance per Square Foot': 'float32', 'Bankruptcy Date': 'category', 'Bankruptcy Indicator': 'category', 'Number Of Installments Paid': 'float32', 'Number Of Remaining Installments': 'int64', 'Deal Type': 'category', 'Original Loan Amount': 'float32', 'Original LTV': 'float32', 'Master Servicer ': 'category', 'NOI': 'float32', 'Occupancy Rate': 'float32', 'Original Amortization Term Months': 'uint16', 'Original Interest Only Term': 'float32', 'Debt Yield': 'float32', 'DSCR': 'float32', 'DSCR At Cutoff': 'float32', 'Loan Originator': 'category', 'Remaining Interest Only Term': 'float32', 'Units': 'float32', 'Coupon': 'float32', 'Borrower Name': 'category', 'Trepp Loan ID': 'category', 'Securitized LTV': 'float32', 'Factor': 'float32', 'Total Number Of Installments': 'uint16'}
loan = load_cmbs(file=irp_loan, main_folder=sup_main_dir, dtype=loan_dtype_practical)

loan_dates = ['Maturity Date', 'Most Recent Appraisal Date',
              'Most Recent Assumption Date', 'Most Recent End Date']

for date in loan_dates:
	date_convert(loan, date)
              
loan['app_upb'] = loan['Most Recent Appraised Value'] - loan['Current Balance Amount']


# IRP PROPERTY DF
prop_dtype_practical = {'Deal ID': 'object', 'Pros ID': 'object', 'Property Number': 'category', 'Tape Date': 'category', 'Servicer Loan ID': 'object', 'Servicer Prospectus Loan ID': 'object', 'Property Name': 'object', 'Property Address': 'object', 'Property Square Feet': 'float32', 'Date Lease Rollover Review': 'category', 'Percent Expiring 1-12 months': 'float32', 'Percent Expiring 13-24 months': 'float32', 'Percent Expiring 25-36 months': 'float32', 'Percent Expiring 37-48 months': 'float32', 'Largest Tenant Name': 'object', 'Largest Tenant Square Feet': 'float32', 'Largest Tenant Lease Expiration': 'object', 'Second Largest Tenant Name': 'object', 'Second Largest Tenant Square Feet': 'float32', 'Second Largest Tenant Lease Expiration': 'object', 'Third Largest Tenant Name': 'object', 'Third Largest Tenant Square Feet': 'float32', 'Third Largest Tenant Lease Expiration': 'object', 'Fourth Largest Tenant Name': 'object', 'Fourth Largest Tenant Square Feet': 'float32', 'Fourth Largest Tenant Lease Expiration': 'object', 'Fifth Largest Tenant Name': 'object', 'Fifth Largest Tenant Square Feet': 'float32', 'Fifth Largest Tenant Lease Expiration': 'object', 'Property Type': 'category', 'Current Balance': 'float32', 'State': 'category', 'Year Built': 'float32', 'Year Renovated': 'float32', 'ZIP': 'category', 'City': 'category', 'Ground Lease Indicator': 'float32', 'Credit Tenant Lease': 'category'}
prop = load_cmbs(file=irp_prop, main_folder=sup_main_dir, dtype=prop_dtype_practical)
prop_active = prop.loc[prop['Current Balance'] > 0,:]

# Load Listings File:
cs = load_cmbs(file=listings_file, main_folder=listings_dir)


# Use the IRP Property file and search tenant name.
def tenant_search(df, tenant):
    """
    Search for Tenant Names in the IRP Property File.

    Search utilizes .str.contains() method on each
    Tenant Column/Series.

    Parameters
    ----------
    df : DataFrame
        DataFrame object (IRP Property file)
        with the default 'Largest Tenant' columns
    tenant : string
        Literal string or regex pattern.

    Returns
    -------
    Dataframe with rows containing Tenant Name.

    Example
    -------
    >> toys_names = "(toys r us|toys r' us|babies r us|babies r' us)"
    >> toys_df = tenant_search(df=prop, tenant=toys_names)
   """
    return df.loc[
        (df['Largest Tenant Name'].str.contains(tenant, case=False))
        | (df['Second Largest Tenant Name'].str.contains(tenant, case=False))
        | (df['Third Largest Tenant Name'].str.contains(tenant, case=False))
        | (df['Fourth Largest Tenant Name'].str.contains(tenant, case=False))
        | (df['Fifth Largest Tenant Name'].str.contains(tenant, case=False)),
        :]

def searchu(df=cmbs, nm='\w', add='\w', cy= '\w', st='\w', pr='\w'):
    """
    Search Lead Generator file for Loan/Property. 

    All parameters, other than df (dataframe), have default
    values that match any alphanumeric character.
    All parameters are case-insensitive.

    Parameters
    ----------
    nm: str
        Search Loan/Property Name column.
    add: str
        Search Address column.
    cy: str
        Search City column.
    st: str
        Search State column.
    pr: str
       Search Property Type column. All Property Type values
       must be one of the following string values...
       'multi-family', 'retail', 'industrial', 'office',
       'hotel' or 'other'.

    Returns
    -------
    DataFrame indexed by string parameters.

    Notes
    -----
    CMBS Universe file (Lead Generator files) will not have
    address values for loans backed by multiple properties.
    Search the Property File (Data Export file) for properties
    that are one of many that serve as the collateral for a
    CMBS loan.
    """
    
    return df.loc[(df['Loan Name'].notnull())
                  & (df['Loan Name'].str.contains(nm, case=False))
                  & (df['Address'].str.contains(add, case=False))
                  & (df['City'].str.contains(cy, case=False))
                  & (df['State'].str.contains(st, case=False))
                  & (df['Property Type'].str.contains(pr, case=False)),
                  ['Deal ID', 'Servicer Loan ID', 'Loan Name',
                   'Address', 'City', 'State', 'Property Type',
                   'Origination Date', 'Maturity Date / ARD',
                   'Current Loan Balance', 'Loan Status',
                   'MR SS Xfer Date']]


def searchp(df=prop_active, nm='\w', add='\w', cy= '\w', st='\w', pr='\w'):
    """
    Search IRP Property file for Property Name. 

    All parameters, other than df (dataframe), have default
    values that match any alphanumeric character.
    All parameters are case-insensitive.

    Parameters
    ----------
    nm: str
        Search Property Name column.
    add: str
        Search Address column.
    cy: str
        Search City column.
    st: str
        Search State column.
    pr: str
       Search Property Type column. All Property Type values
       must be one of the following string values...
       'multi-family', 'retail', 'industrial', 'office',
       'hotel' or 'other'.

    Returns
    -------
    DataFrame indexed by string parameters.

    Notes
    -----
    The IRP Property will not have all the Agency loans in
    the lead generator files.
    Also, the Property name does not always equal the loan name,
    so it is important to know the difference.
    """
    return df.loc[(df['Property Name'].notnull())
                  & (df['Property Name'].str.contains(nm, case=False))
                  & (df['Property Address'].str.contains(add, case=False))
                  & (df['City'].str.contains(cy, case=False))
                  & (df['State'].str.contains(st, case=False))
                  & (df['Property Type'].str.contains(pr, case=False)),
                  ['Deal ID', 'Servicer Loan ID', 'Property Name',
                  'Property Address', 'City', 'State', 'Property Type',
                  'Current Balance']]

bad_words = r"(ave|avenue|way|boulevard|blvd|creek|park|"\
"properties|prop|pky|fwy|"\
"highway|hwy|parkway)"

# can call next on ab = listing_rows(cs). next(ab)
def listing_rows(df):
    for row in df.itertuples():
        """ Assigns & Prints Listing in Format: Address, City, State, Property Type """
        record = row[0]
        address= row[1]
        city = row[2]
        state = row[3]
        prop_type = row[6]
        address_list = [x for x in address.split() if x not in bad_words]
        it = iter(address_list)
        max_len_str = len(max(address_list, key=len))
        for i in range(len(address_list)):
            if len(address_list[i]) < max_len_str or address_list[i] in bad_words:
                next(it)
            else:
                print('\n')
                print("Listing Address: {}, {}, {}, {}".format(address, city, state, prop_type))
                print("Record: {} ".format(record))
                print("Word: {} ".format(address_list[i]))
                print('\n')
                yield search_all(add=next(it), st=state, pr=prop_type)


# WATCHLIST CODE:
# WL dictionary
wl_data = {'1A': 'Over 2 Payments Due',
           '1B': 'Delinquent Taxes',
           '1C': 'Delinquent Insurance',
           '1D': 'Outstanding Servicing Advances',
           '1E': 'NCF DSCR < 1.10; < 1.20 for Health & Lodging',
           '1F': 'NCF DSCR < 1.40 & < 75% UW DSCR',
           '1G': 'Floating Rate Deal: DSCR < 1.0 and < 90% of UW NOI',
           '1H': 'Defaulted Lien in Excess of 5% of UPB',
           '1I': 'Failure to Submit Financial Statements',
           '2A': 'Required Repair not completed by Due Date',
           '2B': 'No Longer in Use',
           '2C': 'Occurence of Servicing Trigger Event',
           '2D': 'Impending Ground Lease Maturity or GL Default',
           '2F': 'Operating License or Franchise Agreement Default',
           '2G': 'Bankruptcy of Borrower/Owner/Guarantor',
           '2H': 'Nursing Home Survey not received',
           '3A': 'Poor Inspection report',
           '3B': 'Property Affected by Life Safety Issue or Potentially Harmful Environmental Issue',
           '3C': 'Property Affected by Major Casualty or Condemnation Proceeding Affecting Future CF',
           '4A': 'Occupancy Decrease, Excludes Lodging',
           '4B': 'No Longer In Use',
           '4C': 'Single Tenant with A Lease > 30% NRA, Expiring within the next 6-12 mos',
           '4D': 'A combination of top 3 tenants with lease expirations within next 6 months',
           '4E': 'Bankruptcy of Licensee, Franchisor or any Combination of Top 3 Tenants > 30% NRA',
           '4F': 'Major Tenant Lease is in Default, Terminated or is Dark',
           '5A': 'Pending Loan Maturity or ARD',
           '6A': 'Any Other Situation that increases Risk of Default and/or losses to Investors',
           '7A': 'Loan has been Returned from the Special Servicer',
           '7B': 'B note was created, or Cumulative Interest shortfalls, or WODRA repayment Periods'
           }

def geo_graph(df, title):
    lat = df['latitude'].values
    lon = df['longitude'].values
    fig = plt.figure(figsize=(8,8))
    m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
                projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
    m.readshapefile('st99_d00', name='states', drawbounds=True)
    m.scatter(lon, lat, latlon=True, cmap='Reds', alpha=0.50, s=15)
    plt.title(title)
    plt.show()

# Bar Graph Function
def cmbs_bars(dict_data, ylim_high, ylabel, ylim_low=0, title='',
              y_thousands=True, text_message='', text_c1=0, text_c2=0,
              style='seaborn-bright', bar_color='darkblue', xtick_rotation=0,
              xtick_font='large', facecolor='lightgray', grid_line_style='-',
              grid_line_width=0.5, grid_color='gray'):
    """
    Create Bar Graph from dictionary.

    Creates Bar Graph from dictionary using Matplotlib.pyplot library
    and allows granular aesthetic specifications.

    Parameters
    ----------
    dict_data : dict
        Of the form {'label' : int} where 'label' are the x-labels
        and int are the y-values.
    ylim_high : int
        Set max y-value displayed.
    ylabel : str
    ylim_low : int, default 0, of course.
    title : str, default ''
    y_thousands : boolean, default True
        Format y-axis values to have thousands separator.
    text_message : str, default ''
        Text annotation to accompany graphic.
    text_c1 : int, default 0
        X-coordinate of text_message.
    text_c2 : int, default 0
        Y-coordinate of text_message.
    style : str, default 'seaborn-bright'
    bar_color : str, default darkblue
    xtick_rotation : int, default 0
    xtick_font : str, default 0
    facecolor : str, default 'lightgray'
    grid_line_style : str, default '-'
    grid_line_width : float, default 0.5
    grid_color : str, default 'gray'

    Returns
    -------
    matplotlib bar plot
    """
    
    data = sorted(dict_data.items(), key=lambda x: x[1], reverse=True)
    data_keys = [key[0] for key in data]
    data_index = range(len(data_keys))
    data_values = [value[1] for value in data]
    plt.style.use(style)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.bar(data_index, data_values, align='center', color=bar_color)
    plt.xticks(data_index, data_keys, rotation=xtick_rotation,
               fontsize=xtick_font)
    ax1.set_ylim(ylim_low, ylim_high)
    plt.ylabel(ylabel)
    plt.text(text_c1, text_c2, text_message)
    plt.title(title)
    ax1.set_facecolor(color=facecolor)
    ax1.grid()
    ax1.grid(linestyle=grid_line_style, linewidth=grid_line_width,
             color=grid_color)
    ax1.set_axisbelow(True)
    if y_thousands:
        ax1.get_yaxis().set_major_formatter(
            plt.FuncFormatter(
                lambda x, loc: "{:,}".format(int(x)))
            )
    plt.show()

def cmbs_pie(xpie, ypie, x_name, y_name, title='', title_size=15, title_y=0.9,
             x_color='darkblue', y_color='lightgray', text_size='large',
             text_color='white', ha_align='center', va_align='top',
             font_weight='bold', autotext_size='large', autotext_color='white'):
    """
    Create Pie Chart from two values.

    Creates Pie Chart to show subset B as a proportion of A.

    Parameters
    ----------
    xpie : int
    ypie : int
    x_name : str
    y_name : str
    title : str, default ''
    title_size : int, default 15
    title_y : int, default 0.9
    x_color : str, default 'darkblue'
    y_color : str, default 'lightgray'
    text_size : str, default 'large'
    text_color : str, default 'white'
    ha_align : str, default 'center'
        Sets horizontal alignment.
    va_align : str, default 'top'
        Sets vertical alignment.
    font_weight : str, default 'bold'
    autotext_size : str, default 'large'
    autotext_color : str, default 'white'

    Returns
    -------
    matplotlib pie chart.
    """
    
    plt.rc('font', weight=font_weight)
    xpie = xpie
    ypie = ypie
    groups = [x_name, y_name]
    fracs = [xpie, ypie]
    patches, texts, autotexts = plt.pie(fracs, labels=groups, autopct='%1.1f%%',
                                        colors=[x_color, y_color])
    [text.set_size(text_size) for text in texts]
    [text.set_color(text_color) for text in texts]
    [text.set_horizontalalignment(ha_align) for text in texts]
    [text.set_verticalalignment(va_align) for text in texts]
    [text.set_path_effects([path_effects.Stroke(linewidth=2, foreground='black'),
                            path_effects.Normal()]) for text in texts]
    [autotext.set_path_effects([path_effects.Stroke(linewidth=2, foreground='black'),
                            path_effects.Normal()]) for autotext in autotexts]
    [autotext.set_size(autotext_size) for autotext in autotexts]
    [autotext.set_color(autotext_color) for autotext in autotexts]
    plt.suptitle(title, fontsize=title_size, y=title_y)
    plt.show()
    plt.rc('font', weight='normal')
