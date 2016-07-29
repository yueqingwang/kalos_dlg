# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 09:33:48 2016

@author: wangyueqing
"""
import re
import datetime

def unit_convert(unit):
    c = re.match(r'([n|u|m]*)\w+',unit)
    if c.group(1) == 'n':
        return 1
    else:
        if c.group(1) == 'u':
            return 1000
        else:
            if c.group(1) == 'm':
                return 1000000
            else:
                return 1000000000
        
        
def PMU_Force(unit):
    if unit == 'V' or unit == 'mV' or unit == 'uV' :
        return 'U'
    if unit == 'A' or unit == 'mA' or unit == 'uA' :
        return 'I'
        
def PMU_Test(a):
    r = '\s+(\S+)\s+(\w+)\s+(\w+)\s+'
    r+= '(-*\d+\.*\d*)\s*([A-Za-z]+)/(-*\d+\.*\d*)\s*([A-Za-z]+)\s+'*3
    r+= '(\w+)'
    m = re.match(r,a)
    if m :
        TestPin = m.group(2)
        TestDes = m.group(3)
        Force = float(m.group(4))
        Force_R = float(m.group(6))
        Measure = float(m.group(8))
        Measure_R = float(m.group(10))
        Max_L  = float(m.group(12))
        Min_L = float(m.group(14))
        PMU = PMU_Force(m.group(5))
        Unit = m.group(9)
        PMUResult = m.group(16)
        return (TestPin,TestDes,PMU,Unit,Force,Force_R,Measure,Measure_R,Max_L,Min_L,PMUResult)
    else:
        return -1
        
def AC_Test(TestFlow,TestID):
    count = 0
    while(1):
        count += 1
        TestID += 1
        if re.match(r'Test ',TestFlow[TestID]) or re.match(r'Kalos2 ',TestFlow[TestID]):
            return 0
        c = re.match(r'.*=\s*([0-9\.]+)\s*([n|u|m]*s+)',TestFlow[TestID])
        if c :
            return float(c.group(1)),c.group(2)
        if count > 10 :
            break

def DataFile_convert(filename):
    f = open(filename,'r')
    TestFlow=[]
    line = f.readline()
    while(line):
        site = []
        if re.match(r'Tester ID:',line):
            site.append(line)
            while(1):
                line2 = f.readline()
                if line2 != '\n' :
                    site.append(line2)
                if re.match(r'Kalos2 ',line2):
                    break
        if site :
            TestFlow.append(site)
        line = f.readline()
    f.close()
    return TestFlow
       
def GetData(filename):
    f = open(filename,'r')
    TestFlow=[]
    FlowIDs=[]
    TestIDs=[]
    for line in f.readlines():
        if line != '\n':
            TestFlow.append(line)
            if re.match(r'Tester ID:',line):
                FlowIDs.append(len(TestFlow)-1)
                TestIDs.append([])
            if re.match(r'Test ',line):
                TestIDs[len(FlowIDs)-1].append(len(TestFlow)-1)
        else:
            next
    f.close()
    return TestFlow,FlowIDs,TestIDs
    
def GetFlowInfo(TestFlow,FlowID):
     m = re.match(r'Tester ID: (\w+-\d+)\s+Date: (\w+ \d+,\d+ \d+:\d+\w+)\n',TestFlow[FlowID])
     Tester_ID = m.group(1)
     c = datetime.datetime.strptime(m.group(2),'%B %d,%Y %I:%M%p')
     Test_Date=c.strftime('%Y-%m-%d %H:%M')
     m = re.match(r'Program: (\w+)\s+Device: (\w+)\s+Flow: (\w+)\s+Serial: (\d+)\n',TestFlow[FlowID+1])
     Program = m.group(1)
     #Device = m.group(2)
     Flow = m.group(3)
     m = re.match(r'Kalos2: (\w+)\s+Lot: (.+)\n',TestFlow[FlowID+2])
     DUT_ID = m.group(1)
     return (Tester_ID,Test_Date,Program,Flow,DUT_ID)
     
def GetFlowResult(TestFlow,FlowID):
    if FlowID >=2 :
        m = re.match(r'.*Total Test Time =([0-9\.]+) s',TestFlow[FlowID-2])
        Flow_time = float( m.group(1) )
        m = re.match(r'Kalos2 .*Result=(\w+), SortBin=(\d+), SoftBin=(\d+)',TestFlow[FlowID-1])
        Flow_Result = m.group(1)
        SortBin = m.group(2)
        return Flow_time,Flow_Result,SortBin
    else:
        return 0
        
def GetDesc(fns):
    Desc = fns[0]
    Wafer_ID = None
    Device = None
    if  len(fns) > 1:
        Device = fns[-1]
    if Desc == '一致性' :
        Wafer_ID = fns[1]
    return Desc,Wafer_ID,Device
        
    
        
def IDcreate(Device,Test_Date,FlowOrder,TestOrder):
    c = datetime.datetime.strptime(Test_Date,'%Y-%m-%d %H:%M')
    t = c.strftime('%y%m%d%H%M')
    return "D%s_%s_%02d_%02d" % (Device,t,FlowOrder,TestOrder)
    
    
def GetTestName(TestFlow,TestID):
    return TestFlow[TestID].split()[-1]
    
def GetAcDcTestResult(TestFlow,TestID,Test_Type):
    if Test_Type == 'DC':
        Measure = PMU_Test(TestFlow[TestID+2])[6]
        Test_R =  PMU_Test(TestFlow[TestID+2])[10]
        Unit = PMU_Test(TestFlow[TestID+2])[3]
        return Measure,Test_R,Unit
    else:
        Measure,Unit = AC_Test(TestFlow,TestID)
        Test_R =  'PASS'
        return Measure,Test_R,Unit
        
    
#print(unit_convert('ns'))

#def GetAcTime()
    
#print( IDcreate('2016-07-15 13:27',1,1) )
    


#f = open('0C.dlg','r')
#TestFlow=[]
#line = f.readline()
#while(line):
#    site = []
#    if re.match(r'Tester ID:',line):
#        site.append(line)
#        while(1):
#            line2 = f.readline()
#            if line2 != '\n' :
#                site.append(line2)
#            if re.match(r'Kalos2 ',line2):
#                break
#    if site :
#        TestFlow.append(site)
#    line = f.readline()
#
#f.close()

#TestFlow,FlowIDs,TestIDs = GetData('0C.dlg')
#print(len(TestFlow),FlowIDs,TestIDs)
#
#
#for FlowID in FlowIDs:
#    print(GetFlowInfo(TestFlow,FlowID))


#Tester_ID = 0
#Date = 0
#Program = 0 
#Device = 0
#Flow = 0 
#Serial = 0
#DUT_ID = 0  
#Lot = 0
#Operator = 0
#DibPart = 0
#DibSerial = 0
#Vendor = 0
#System = 0 
#Comment = 0
#Users_C = 0



#for line in TestFlow:
#    if re.match(r'Tester ID: (\w+-\d+)\s+Date: (\w+ \d+,\d+ \d+:\d+\w+)\n',line) :
#        m = re.match(r'Tester ID: (\w+-\d+)\s+Date: (\w+ \d+,\d+ \d+:\d+\w+)\n',line)
#        Tester_ID = m.group(1)
#        c = datetime.datetime.strptime(m.group(2),'%B %d,%Y %I:%M%p')
#        Date=c.strftime('%Y-%m-%d %H:%M')
#    if re.match(r'Program: (\w+)\s+Device: (\w+)\s+Flow: (\w+)\s+Serial: (\d+)\n',line) :
#        m = re.match(r'Program: (\w+)\s+Device: (\w+)\s+Flow: (\w+)\s+Serial: (\d+)\n',line)
#        Program = m.group(1)
#        Device = m.group(2)
#        Flow = m.group(3)
#        Serial = m.group(4)
#    if re.match(r'Kalos2: (\w+)\s+Lot: (.+)\n',line) :
#        m = re.match(r'Kalos2: (\w+)\s+Lot: (.+)\n',line)
#        DUT_ID = m.group(1)
#        Lot = m.group(2)
#    if re.match(r'Operator: (\w+)\n',line) :
#        m = re.match(r'Operator: (\w+)\n',line)
#        Operator = m.group(1)
#    if re.match(r'DibPart: (\w+)\n',line) :
#        m = re.match(r'DibPart: (\w+)\n',line)
#        DibPart = m.group(1)
#    if re.match(r'DibSerial: (\w+)\n',line) :
#        m = re.match(r'DibSerial: (\w+)\n',line)
#        DibSerial = m.group(1)
#    if re.match(r'Vendor: (\w+)\n',line) :
#        m = re.match(r'Vendor: (\w+)\n',line)
#        Vendor = m.group(1)
#    if re.match(r'System: (\w+)\n',line) :
#        m = re.match(r'System: (\w+)\n',line)
#        System = m.group(1)
#    if re.match(r'Comment: (\w+)\n',line) :
#        m = re.match(r'Comment: (\w+)\n',line)
#        Comment = m.group(1)
#    if re.match(r'Users_C: (\w+)\n',line) :
#        m = re.match(r'Users_C: (\w+)\n',line)
#        Users_C = m.group(1)
#        break
#
#        
#a = TestFlow[24] 
#print(a)
#
#print(PMU_Test(a))


#print(Tester_ID)
#print(Date)
#print(Program)
#print(Device)
#print(Flow)
#print(Serial)
#print(DUT_ID)
#print(Lot)
#print(Operator)
#print(DibPart)
#print(DibSerial)
#print(Vendor)
#print(System)
#print(Comment)
#print(Users_C)
