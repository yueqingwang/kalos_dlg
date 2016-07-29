#encoding=utf-8
#甄码农 python 示例代码
#glob 用通配符查找指定目录中的文件
import os
import glob
import re
 
def findfiles(pattern,*params):
    cwd = os.getcwd() #保存当前工作目录
    result = []
    DirList =[]
    if params :
        DirList=list(params)
    else:
        DirList.append(cwd)

    for dirname in DirList:
        os.chdir(dirname)
        for filename in glob.glob(pattern): #此处可以用glob.glob(pattern) 返回所有结果
            filename=dirname+'\\'+filename
            result.append(filename)
        #恢复工作目录
        os.chdir(cwd)
        
    return result
    
def findallfiles(pattern,files,*params):
    tempfiles = findfiles(pattern,*params)
    for fi_d in tempfiles:
        if os.path.isdir(fi_d):
            findallfiles(pattern,files,fi_d)
        else:
            files.append(fi_d)
 
if __name__ == '__main__':
    files =[]
    findallfiles('*',files,'D:\python\kalos_dlg\功能性能分析数据')
    for i in files:
        c = re.match('.*\\\\功能性能分析数据\\\\(.*)\.dlg',i) 
        if c :
            d = c.group(1)
            a=d.split('\\')
            print(a)