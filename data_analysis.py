import pandas as pd
from functools import reduce
import numpy

io = 'D:/项目/HL28/Data_parse/BT01426_tidy_data.xlsx'
io1 = 'D:/项目/HL28/HL_wafer_list.xlsx'
io2 = 'D:/项目/HL28/HL28_CP_config.xlsx'


data = pd.read_excel(io)
conner = pd.read_excel(io1)
bin = pd.read_excel(io2,sheet_name='01.M125_softbin')

data = data.iloc[:,[1,2,3,4,5,6,7,8,9]]
data = data.rename(columns = {'WaferID':'Wafer'})

bin_df = bin[['HardBin','SoftBin','Bin']]
bin.drop_duplicates(['HardBin','SoftBin','Bin'])[['HardBin','SoftBin','Bin']]
bin_df = bin_df.dropna()
bin_df.columns = ['Hardbin','Softbin','bin']

conner_df = conner[['Lot','WaferID','Wafer','Corner']]
conner_df['WaferID'].astype(str)

n_chip = len(data.drop_duplicates(['locate_X','Locate_Y'])[['locate_X','Locate_Y']])


aa = pd.merge(data, bin_df ,how = 'inner', on=['Hardbin','Softbin'])
aa = pd.merge(aa, conner_df ,how = 'inner', on=['Wafer'])
aa = aa.drop_duplicates()

file_name = aa['Wafer'][0].split('_')[0] + '_CP_analysis_data.xlsx'
aa = aa.rename(columns = {'temp':'Temperature','Start':'Date','bin':'Bin','Lot_x':'Lot'})


col_list = ['Date','program',  'Temperature', 'Wafer', 'locate_X', 'Locate_Y', 'Hardbin','Softbin',
       'Bin', 'Lot', 'WaferID', 'Corner']
aa = aa[col_list]



with pd.ExcelWriter(file_name, engine='xlsxwriter', mode='w') as writer:
       aa.to_excel(writer, sheet_name='SOF_Bin',index=False)