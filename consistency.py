# -*- coding: utf-8 -*-

import numpy as np
import sqlite3
import pandas as pd 
import matplotlib.pyplot as plt
import re
#from pylab import mpl
#mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
#mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题


def datafetch(data):
    index = [i[0] for i in data]
    sdata = [i[1]/1000000 for i in a]
    return index,sdata

conn = sqlite3.connect('test.db')
curs = conn.cursor()

def GetStat(data,testname):
    dcount = len(data)
    dmax = np.max(data)
    dmin = np.min(data)
    dmean = np.mean(data)
    dstd = np.std(data)
    dup = dmean + dstd
    ddown = dmean - dstd
    m=0
    if dmean > 500000000:
        n = 1000000000
        m = ' '
    else:
        if dmean > 500000:
            n=1000000
            m = 'm'
        else:
            if dmean > 500 :
                n=1000
                m='u'
            else:
                n=1
                m='n'
    if re.match('.*I.*',testname):
        m=m+'A'
    else:
        m=m+'s'
    return m,dcount,dmax/n,dmin/n,dmean/n,dstd/n,dup/n,ddown/n
    
dd=curs.execute('''SELECT DISTINCT Wafer_ID FROM ACDC_RESULT 
                INNER JOIN TEST_FLOW ON ACDC_RESULT.ID = TEST_FLOW.ID
                WHERE  Desc='一致性' ''')    
wafer_id = [i[0] for i in dd.fetchall()]

dd=curs.execute('''SELECT DISTINCT Test_Name FROM ACDC_RESULT 
                INNER JOIN TEST_FLOW ON ACDC_RESULT.ID = TEST_FLOW.ID
                WHERE  Desc='一致性' ''')    
testname = [i[0] for i in dd.fetchall()]


columns = ['单位','样本数','最大值','最小值','平均值','标准偏差','＋1σ','－1σ']
for wd in wafer_id:
    frame = []
    for tn in testname:
        query = ''' SELECT Device,Measure FROM ACDC_RESULT 
                        INNER JOIN TEST_FLOW ON ACDC_RESULT.ID = TEST_FLOW.ID
                        WHERE   Desc='一致性' AND Wafer_ID = '{}' 
                        AND Test_Name ='{}' '''.format(wd,tn)            
        dd = curs.execute(query)
        meas= [i[1] for i in dd.fetchall()]
        frame.append( GetStat(meas,tn) )
        
    data = pd.DataFrame(frame,index=testname,columns = columns )       
    data.to_csv('%s.csv' % wd)

conn.close()