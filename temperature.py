# -*- coding: utf-8 -*-

import numpy as np
import sqlite3
import pandas as pd 
import matplotlib.pyplot as plt
import re


def datafetch(data):
    index = [i[0] for i in data]
    sdata = [i[1]/1000000 for i in a]
    return index,sdata

conn = sqlite3.connect('test.db')
curs = conn.cursor()

query = ''' SELECT Temperatures,DUT_ID,Test_Name,Measure,Unit FROM ACDC_RESULT 
        INNER JOIN TEST_FLOW ON ACDC_RESULT.ID = TEST_FLOW.ID
        WHERE   Desc='温度曲线' 
        ORDER BY Temperatures'''

dd = curs.execute(query)
a = dd.fetchall()
data = pd.DataFrame(a,columns = ['温度','DUT','测试项','数据','单位'])
data = pd.pivot_table(data, values='数据', index=['温度'], columns=['测试项','DUT','单位'])
#data.to_csv('temperature.csv')
#print(data['测试项'])
for tn in data.columns.levels[0]:
    pdata = data[tn]
    plt.plot(pdata,'-o')
    #print(pdata.columns)
    plt.legend([i[0] for i in pdata.columns],loc = 0)
    mm = re.match('\w+_(\w+)_\w+',tn)
    ylabel = mm.group(1)+' ({})'.format(pdata.columns[0][1])
    xlabel = u'Temperature ($^\circ$C)'
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.grid()
    plt.savefig(tn+'.tif',dpi=300,format = 'tif')
    plt.clf()

conn.close()