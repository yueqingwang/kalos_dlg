# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 12:47:00 2016

@author: wangyueqing
"""

import numpy as np
import sqlite3
import pandas as pd 
import matplotlib.pyplot as plt
import re

def data_uni(t,n):
    unit={' ':1000,'m':1,'u':1e-3,'n':1e-6}
    mm = re.match('([n|u|m|\s]{1})\w+',n)
    bias = 1
    if mm :
        bias = unit[mm.group(1)]
    return bias*t
    
def unit_uni(t):
    return re.sub('[n|u|m|\s]+','m',t)
    
def freq(t):
    t1 = re.sub('^0','0.',t)
    t2 = re.sub('M','',t1)
    return float(t2)



conn = sqlite3.connect('test.db')
conn.create_function("uni", 1, unit_uni)
conn.create_function("dni", 2, data_uni)
conn.create_function("dfre", 1, freq)
curs = conn.cursor()

query = ''' SELECT dfre(Freq),DUT_ID,Test_Item,dni(Measure,Unit),uni(Unit) FROM ACDC_RESULT 
        INNER JOIN TEST_FLOW ON ACDC_RESULT.ID = TEST_FLOW.ID
        WHERE   Desc='频率特性' 
        ORDER BY Freq'''

dd = curs.execute(query)
a = dd.fetchall()
data = pd.DataFrame(a,columns = ['频率','DUT','测试项','数据','单位'])
data = pd.pivot_table(data, values='数据', index=['频率'], columns=['测试项','DUT','单位'])

data.to_csv('freq.csv')
for tn in data.columns.levels[0]:
    pdata = data[tn]
    print(pdata)
    plt.plot(pdata,'-o')
    #print(pdata.columns)
    plt.legend([i[0] for i in pdata.columns],loc = 0)
    ylabel = tn+' ({})'.format(pdata.columns[0][1])
    xlabel = u'Frequency (MHz)'
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.grid()
    plt.savefig(tn+'.tif',dpi=300,format = 'tif')
    plt.clf()

conn.close()