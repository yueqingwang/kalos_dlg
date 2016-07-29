# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:47:27 2016

@author: wangyueqing
"""

import numpy as np
import sqlite3
import pandas as pd 
import matplotlib.pyplot as plt
import re


conn = sqlite3.connect('test.db')
curs = conn.cursor()

query = ''' SELECT DPS,DUT_ID,Test_Item,Measure,Unit FROM ACDC_RESULT 
        INNER JOIN TEST_FLOW ON ACDC_RESULT.ID = TEST_FLOW.ID
        WHERE   Desc='电源电压曲线' 
        ORDER BY DPS'''

dd = curs.execute(query)
a = dd.fetchall()
data = pd.DataFrame(a,columns = ['电压','DUT','测试项','数据','单位'])
data = pd.pivot_table(data, values='数据', index=['电压'], columns=['测试项','DUT','单位'])
data.to_csv('temperature.csv')
for tn in data.columns.levels[0]:
    pdata = data[tn]
    plt.plot(pdata,'-o')
    #print(pdata.columns)
    plt.legend([i[0] for i in pdata.columns],loc = 0)
    #mm = re.match('\w+_(\w+)_\w+',tn)
    ylabel = tn+' ({})'.format(pdata.columns[0][1])
    xlabel = u'DPS (V)'
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.xlim(2.9,3.7)
    plt.grid()
    plt.savefig(tn+'.tif',dpi=300,format = 'tif')
    plt.clf()

conn.close()