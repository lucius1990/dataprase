import pandas as pd
from functools import reduce
import numpy

io = 'D:/项目/HL28/Sapphire28_M125_CP/BT01426/outPut_PF.csv'
data = pd.read_csv(io)
drop_col = ['File','SubLot','TestCode','TestFlow','tester','Dut','SITE','Testtime','TestCount','RC']
data = data.drop(columns=drop_col)
t = data['Start'].str.split(expand=True)
data['Start'] = t[0]
# t = data['program'].str.split('//',expand=True)
# data['program'] = t[1]
# t = data['WaferID'].str.replace('#','_').str.split('-',expand=True)
# data['WaferID'] = t[0]
data['WaferID'] = data['Lot'].str.cat('_'+data['WaferID'].astype(str))
data = data.replace(['PASS','FAIL'],[1,0])
data.to_excel('BT01426_tidy_data.xlsx')