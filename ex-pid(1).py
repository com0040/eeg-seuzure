# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 20:21:33 2022

@author: chang
"""
import os # 파일을 복사하거나 디렉터리를 생성하고 특정 디렉터리 내의 파일 목록 구하기
import csv
import pandas as pd # 행과 열로 구성된 객체 생성, 안정적 데이터 처리
 # import matplotlib.pyplot as plt # 시각화 패키지
import numpy as np # 고성능 과학 계산용 패키지
import natsort
import sys
from pandas import DataFrame
import datetime as dt
# from pidlist import pidlist # pidlist 파일에서 함수 전부 가져오기


path2 = 'C:/Users/chang/Desktop/rader_PID/example/ex/'

filePath = 'C:/Users/chang/Desktop/rader_PID/example/'   # 폴더 주소를 입력
fileall = os.listdir(filePath) # 경로내에 있는 파일모두 불러서 리스트화
fileCsv = [filePath + f[:-4] for f in fileall if f.endswith('.csv')] # csv에만 적용해라 f=0번째
#fileCsv = natsort.natsorted(fileCsv) # PID 재정렬(혹시 순서대로 안되있을까봐)
CSVname =[]
listpid =[]
df_new = pd.DataFrame()

for i in range (0,len(fileCsv)): 
    CSVname.append(os.path.basename(str(fileCsv[i]))) # 파일 이름만 저장
    pid = CSVname[i].split("_")    
    listpid.append(pid[0])

    pidx = list(set(listpid))

print(len(CSVname))
for e in range (0,len(pidx)):
    
    print('1' + str(e))
    
    pidpath =[]
    for j in range (0,len(CSVname)):
        CSVsplit = CSVname[j].split("_")
        split0 = CSVsplit[0]        
          
        if pidx[e] == split0:                         
            pidpath.append(filePath + '%s' %(CSVname[j]) + '.csv' )
                     
    df_time = 0
    df_time = int()        
    
    for h in range(0,len(pidpath)):
        df_length = int()            
        df = pd.read_csv(pidpath[h],names = ['1', '2', '3'])
        df_length = len(df)
        df_time = (df_time + df_length) / 500
            
        if df_time > 86400:
            break
        
    df_list =[]
    name_list =[]
    
    print('3' + str(e))
    if df_time <= 86400:
        #for k in range(0,len(pidpath)): 
            
        for l in range(0,len(pidpath)):
            globals()['name%d'%l] = l
            name_list.append('name%d' %l)
                
        print(len(name_list))    
        for name in name_list: # name_list의 인수들을 순서대로 name에 할당
            globals()[name] = pd.read_csv(pidpath[name_list.index(name)], names = ['1', '2', '3']) 
            # 할당받은 name에 name_list중 name이 몇번째인지를 pidpath에 넣어 경로불러 저장 
            df_list.append(globals()[name]) # 
                  
        df_new = pd.concat(df_list)
        print(len(df_new))
    
    if df_time <= 86400:
        df_new.to_csv('%s%s.csv' %(path2,int(pidx[e])), index = False, header = None)