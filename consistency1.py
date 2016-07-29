# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 08:47:54 2016

@author: wangyueqing
"""

import numpy as np
import sqlite3
import pandas as pd 
import matplotlib.pyplot as plt
import re
import sqlite_stat as sqs


conn = sqlite3.connect('test.db')
curs = conn.cursor()

conn.create_aggregate("stdv", 1, sqs.StdevFunc)
conn.create_aggregate("SGP", 1, sqs.sigma_plus)
conn.create_aggregate("SGM", 1, sqs.sigma_minus)

query = ''' SELECT Test_Name,Wafer_ID,Unit,COUNT(Measure),MAX(Measure),
            MIN(Measure),AVG(Measure),stdv(Measure),SGP(Measure),
            SGM(Measure) FROM ACDC_RESULT 
            INNER JOIN TEST_FLOW ON ACDC_RESULT.ID = TEST_FLOW.ID
            WHERE   Desc='一致性' GROUP BY Test_Name,Wafer_ID '''  
                
dd=curs.execute(query)   
ff = dd.fetchall() 

columns = ['单位','样本数','最大值','最小值','平均值','标准偏差','＋1σ','－1σ']
index1 = [i[0] for i in ff]
index2 = [i[1] for i in ff]
fdata = [i[2:] for i in ff]
        
data = pd.DataFrame(fdata,index=[index1,index2],columns = columns)  
data = data.stack()
data = data.unstack(1)
data = data.unstack()
data.to_csv('consist.csv')

conn.close()