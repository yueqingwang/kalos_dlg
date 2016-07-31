# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 16:02:27 2016

@author: wangyueqing
"""

import sqlite3
import re
import FlowData as fd
import custom_file_find as cff
import pandas as pd

def GetTemp(filename):
    m = re.match(r'(-*\d+)C.dlg',filename)
    return int(m.group(1))
    
def GetAcDcItem(testname):
    c = re.match(r'([AC|DC]+)_(\d+M)*(\w+)_V(\d+)$',testname)
    if c:
        return c.groups()
    else:
        return 0
    
conn = sqlite3.connect('test.db')
curs = conn.cursor()

try:
    curs.execute(
    '''CREATE TABLE TEST_FLOW
       ( ID            INT    PRIMARY KEY   NOT NULL,
         Tester_ID     TEXT   ,
         Test_Date     TEXT   ,
         Program       TEXT   ,
         Flow          TEXT   ,
         DUT_ID        TEXT   ,
         Desc          TEXT   ,
         Wafer_ID      TEXT   ,
         Device        TEXT   ,
         Flow_Time     FLOAT  ,
         Flow_Result   TEXT   ,
         SortBin       TEXT   ,
         Test_Name     TEXT   ,
         Test_Order    INT
         );'''
      )
except:
    print("CREATE TABLE TEST_FLOW error")
    
    
try:
    curs.execute(
    '''CREATE TABLE ACDC_RESULT
       ( ID            INT    NOT NULL,
         Temperatures  INT    ,
         DPS           FLOAT  ,
         Freq          INT    ,
         Test_Item     TEXT   NOT NULL,
         Measure       FLOAT  ,
         Test_R        TEXT   ,
         Unit          TEXT
         );'''
      )
except:
    print(" CREATE TABLE ACDC_RESULT error")
    


query = 'INSERT INTO TEST_FLOW VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
query1 = 'INSERT INTO ACDC_RESULT VALUES (?,?,?,?,?,?,?,?)'

filenames =[]
cff.findallfiles('*',filenames,'D:\Workspace\FMSH\Python\kalos_dlg\功能性能分析数据')
#for i in filenames:
#    print(i)
#    c = re.match('.*\\\\功能性能分析数据\\\\(.*)\.dlg',i) 
#    if c :
#        d = c.group(1)
#        a=d.split('\\')
#        print(a)

t_id=0
for id_base in curs.execute('SELECT MAX(ID) FROM TEST_FLOW'):
    if id_base[0]  :
       t_id = id_base[0]
print(t_id)

#frame = []
for filename in filenames:
    c = re.match('.*\\\\功能性能分析数据\\\\(.*)\.dlg',filename)
    if c:
        fns = c.group(1).split('\\')
        TestFlow,FlowIDs,TestIDs= fd.GetData(filename)
        #print(fns)
        #print(len(TestFlow),FlowIDs,TestIDs)
        for i in range(len(FlowIDs)):
            flowinfo = fd.GetFlowInfo(TestFlow,FlowIDs[i])
            #print(flowinfo)
            try:
                flow_result = fd.GetFlowResult(TestFlow,FlowIDs[i+1])
            except IndexError :
                flow_result = fd.GetFlowResult(TestFlow,len(TestFlow))
            #print(flow_result)
            flow_dwd = fd.GetDesc(fns)
            #print(flow_dwd)
            for j in range(len(TestIDs[i])):
                vals =[]
                testname = fd.GetTestName(TestFlow,TestIDs[i][j])
                testorder = j
                #t_id = fd.IDcreate(flow_dwd[-1],flowinfo[1],i,j)
                t_id += 1
                vals.append(t_id)
                vals.extend(flowinfo)
                vals.extend(flow_dwd)
                vals.extend(flow_result)
                vals.append(testname)
                vals.append(testorder)
                #frame.append(vals)
                try:
                    curs.execute(query,vals)
                except:
                    print(vals)
                acdc = GetAcDcItem(testname)
                if acdc :
                   dps = float(acdc[3])/100
                   freq = acdc[1]
                   Test_Item = acdc[2]
                   Temp = None
                   if flow_dwd[0] == '温度曲线' :
                       ff = re.match('(-*[0-9]+)C',flow_dwd[-1])
                       Temp = int(ff.group(1))
                   Measure,Test_R,Unit = fd.GetAcDcTestResult(TestFlow,TestIDs[i][j],acdc[0])
                   vals1 =[t_id,Temp,dps,freq,Test_Item,Measure,Test_R,Unit]
                   #print(vals1)
                   curs.execute(query1,vals1)

#fr = pd.DataFrame(frame)
#fr.to_csv('frame.csv')

conn.commit()
conn.close()

        

    
