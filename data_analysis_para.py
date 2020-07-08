import pandas as pd
from functools import reduce
import numpy

io = 'D:/项目/HL28/Data_parse/BT01426_tidy_data.xlsx'
io1 = 'D:/项目/HL28/Data_parse/BT01426_CP_analysis_data.xlsx'
io2 = 'D:/项目/HL28/HL28_CP_config.xlsx'


data = pd.read_excel(io)
conner = pd.read_excel(io1)
b_type = pd.read_excel(io2)

drop_col = ['Unnamed: 0', 'Lot','Hardbin','Softbin','locate_X','Locate_Y']
n_chip = len(data.drop_duplicates(['locate_X','Locate_Y'])[['locate_X','Locate_Y']])

tt = data.drop(columns = drop_col)
tt = tt.drop(columns = tt.columns[tt.columns.str.contains('Unnamed')])

tt = tt.melt(id_vars=['Start','temp', 'program', 'WaferID'])

tt = tt.rename(columns = {'WaferID':'Wafer'})
b_type = b_type.rename(columns = {'Parameter':'variable'})
c_drop_col = ['Softbin', 'Hardbin', 'Bin', 'locate_X','Locate_Y','Lot','WaferID']
conner = conner.drop(columns = c_drop_col)

aa = tt['value'].groupby([tt['Start'],tt['temp'], tt['program'], tt['Wafer'], tt['variable']]).value_counts(dropna=False)

aa_df = pd.DataFrame(aa)
aa_df = aa_df.unstack(5)
aa_df = aa_df.reset_index()

name = ['Date','Temperature','program','Wafer','variable','NaN','0','1']
aa_df.columns = name


aa_df['FR']=aa_df['0'].fillna(0)/n_chip

aa_df = pd.merge(aa_df, b_type ,how = 'inner', on=['variable'])
aa_df = pd.merge(aa_df,conner,how = 'inner', on = ['Date', 'Temperature', 'program', 'Wafer'])

aa_df = aa_df.drop_duplicates().reset_index()

aa_df = aa_df.drop(columns= ['index'])

d_df_drop = ['Date','NaN', '0','1']
d_df = aa_df.drop(columns= d_df_drop)

d_df['Wafer'] = d_df['Wafer'].str.cat('\n' + d_df['Corner'])

d_df = d_df.drop(columns= 'Corner')

d_df = pd.pivot_table(d_df, index = ['program','Temperature','Bin_Type1','variable'], columns = ['Wafer'], values='FR')
d_df = d_df.reset_index()

file_name = aa_df['Wafer'][0].split('_')[0] + '_CP_analysis_data.xlsx'

aa_df = aa_df.rename(columns= {'variable':'Parameter'} )
col = ['Date',  'Wafer','program', 'Temperature', 'Parameter', 'NaN', '0', '1',
       'FR', 'Corner','Bin_Type1' ]
aa_df = aa_df[col]

d_df = d_df.rename(columns = {'program':'PGM', 'variable':'Parameter'})

with pd.ExcelWriter(file_name, engine='openpyxl', mode='a') as writer:
    aa_df.round(3).to_excel(writer, sheet_name='Param_FR_plot',index=False)
    d_df.round(3).to_excel(writer, sheet_name='Param_FR_reader',index=False)

