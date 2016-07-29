# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 14:32:43 2016

@author: wangyueqing
"""

import numpy as np
import sqlite3
import pandas as pd 
import matplotlib.pyplot as plt
import re
import sqlite_stat as sqs
import beeswarm  as bsw

conn = sqlite3.connect('test.db')
curs = conn.cursor()

def GetColor(x):
    colors = []
    q=np.percentile(x,[25,75])
    w1 = q[1]+(q[1]-q[0])*1.5
    w0 = q[0]-(q[1]-q[0])*1.5
    x.sort()
    for item in x:
        if item > w1 or item < w0: colors.append("orange")
        else: colors.append('yellow')
    return colors

dd=curs.execute('''SELECT DISTINCT Wafer_ID FROM ACDC_RESULT 
                INNER JOIN TEST_FLOW ON ACDC_RESULT.ID = TEST_FLOW.ID
                WHERE  Desc='一致性' ''')    
wafer_id = [i[0] for i in dd.fetchall()]
dd=curs.execute('''SELECT DISTINCT DPS FROM ACDC_RESULT 
                INNER JOIN TEST_FLOW ON ACDC_RESULT.ID = TEST_FLOW.ID
                WHERE  Desc='一致性' ''')    
dps = [i[0] for i in dd.fetchall()]

dd=curs.execute('''SELECT DISTINCT Test_Item FROM ACDC_RESULT 
                INNER JOIN TEST_FLOW ON ACDC_RESULT.ID = TEST_FLOW.ID
                WHERE  Desc='一致性' ''')    
testname = [i[0] for i in dd.fetchall()]

boxprops = dict(linestyle='--', linewidth=3, color='darkgoldenrod')
flierprops = dict(marker='o', markerfacecolor='red', markersize=6,
                  linestyle='none')
medianprops = dict(linestyle='-.', linewidth=2.5, color='firebrick')
meanpointprops = dict(marker='D', markeredgecolor='black',
                      markerfacecolor='firebrick')
meanlineprops = dict(linestyle='--', linewidth=2.5, color='purple')

for wd in wafer_id:
    for tn in testname:
        ix = 0
        frame = []
        xticks =[]
        Unit = 0
        colors=[]
        fig, ax = plt.subplots()
        for dp in dps:
            query = ''' SELECT Test_Item,Wafer_ID,Device,Unit,Measure FROM ACDC_RESULT 
                INNER JOIN TEST_FLOW ON ACDC_RESULT.ID = TEST_FLOW.ID
                WHERE  Desc='一致性' AND Test_Item =? AND Wafer_id=? AND DPS=?''' 
            dd = curs.execute(query,(tn,wd,dp))
            ff = dd.fetchall()
            #columns = ['测试项','wafer_id','芯片编号','单位','数据']
            #data = pd.DataFrame(ff,columns = columns) 
            fdata = [i[4] for i in ff]
            frame.append( fdata )
            xticks.append('{}'.format(dp))
            colors.extend(GetColor(fdata))
            Unit = ff[0][3]
            
        bsw.beeswarm(frame,ax=ax,col=colors)
        box=ax.boxplot(frame,positions = [0,1,2],whis=1.5,showfliers=False,
                medianprops=medianprops,
                meanprops=meanpointprops, meanline=False,showmeans=True)
        plt.xticks( np.arange(3), xticks )
        plt.xlabel( 'DPS (V)' )
        plt.ylabel( '{} ({})'.format(tn,Unit) )
        #plt.xlim(-2,5)
        #plt.ylim(np.min(frame)-np.abs(np.max(frame)*0.1),np.max(frame)+np.abs(np.max(frame))*0.1)
        figname = '%s_%s.tif' % (tn,wd)
        plt.savefig(figname,dpi = 300)
        plt.clf()
        
                
        
conn.close()