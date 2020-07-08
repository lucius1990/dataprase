import pandas as pd
from functools import reduce
import numpy

io = 'D:/项目/HL28/Data_parse/BT01426_CP_analysis_data.xlsx'
io1 = 'D:/项目/HL28/HL_wafer_list.xlsx'
io2 = 'D:/项目/HL28/HL28_CP_config.xlsx'


data = pd.read_excel(io)
conner = pd.read_excel(io1)
bin = pd.read_excel(io2,sheet_name='01.M125_softbin')

n_chip = len(data.drop_duplicates(['locate_X','Locate_Y'])[['locate_X','Locate_Y']])

data = data.drop(columns = ['Hardbin','Softbin','locate_X','Locate_Y'])

t = data.groupby(['Date','Temperature','Wafer','Lot','program','Corner','Bin']).count()



t = t.reset_index()
t = t.rename(columns = {'WaferID':'n','Start':'Date'})
t['value'] = (t['n']/n_chip).round(3)
t['WaferID'] = t['Wafer'].str.split('_').str[1]
data['Wafer'] = data['Wafer'].str.cat('\n' + data['Corner'])
b = data.groupby(['Bin','Wafer','Temperature','program']).count()['Date']/n_chip
b = b.reset_index()
b = pd.pivot_table(b, index = ['Bin','Temperature','program'], columns = ['Wafer'], values='Date')



t = t.rename(columns = {'program':'PGM','value':'Value'})

col_list = ['Date','PGM', 'Temperature', 'Wafer','Bin','WaferID', 'Corner', 'Lot', 'n','Value']
t = t[col_list]

b = b.reset_index()
b = b.rename(columns = {'program':'PGM'})

col = ['PGM','Temperature', 'Bin']
col_list = list(b.columns)
col.extend(col_list[3:])
b = b[col].round(3)

file_name = t['Wafer'][0].split('_')[0] + '_CP_analysis_data.xlsx'

with pd.ExcelWriter(file_name, engine='openpyxl', mode='a') as writer:
    t.to_excel(writer, sheet_name='Yield_trend_SOF',index=False)
    b.fillna('0').to_excel(writer, sheet_name='Yield_trend_SOF_reader',index=False)