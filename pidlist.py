# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 13:26:34 2022

@author: chang
"""

import os # 파일을 복사하거나 디렉터리를 생성하고 특정 디렉터리 내의 파일 목록 구하기
import csv
import pandas as pd # 행과 열로 구성된 객체 생성, 안정적 데이터 처리
    # import matplotlib.pyplot as plt # 시각화 패키지
import numpy as np # 고성능 과학 계산용 패키지
#import natsort # 
#import sys
#import openpyxl # 엑셀편집
from pandas import DataFrame # 판다스 라이브러리-데이터프레임 사용을 위해
import datetime as dt
from tqdm import tqdm

def pidlist(path1,path2): #
        
    filePath = '%s' %(path1)  # 폴더 주소를 path1으로 받아서 저장
    fileall = os.listdir(filePath) # 경로내에 있는 파일모두 불러서 리스트화    
    filename_csv =[f[:-4] for f in fileall if f.endswith('.csv')] # csv파일만 가져오기
    splitCSV = [filename_csv[i].split("_") for i in range(0,len(filename_csv))] # 파일 이름을 분할 [0]에 pid 저장 / [1] 시작시간 저장
    pid = [splitCSV[i][0] for i in range(0,len(splitCSV))]
    
    pidx = list(set(pid)) # pid중 중복되는 것 제거
    # pidx.sort(reverse=True) 
    
    filename='CCU_databa(0)' #파일명 고정값
    output_path= path2 
    
    uniq=1
    while os.path.exists(output_path):  #동일한 파일명이 존재할 때
      output_path='%s%s(%d)' % (path2,filename[:-3],uniq) #파일명(1) 파일명(2)...
      uniq+=1
    
    os.mkdir('%s' %(output_path))
    
    i=1
    for e in range (0,len(pidx)):
        print('중복없는 총 %s개의 pid 중 같은 pid를 한 list로 %s번째 합치기' %(len(pidx),i)) # 중복되지 않은 pid만큼 반복
        i+=1
        pidpath =[filePath + '%s' %(filename_csv[f]) + '.csv' for f in range(0,len(pid)) if pidx[e] == pid[f]] 
        # 같은 pid경로를 리스트로 저장     
        pidpath.sort() # 한 pid에 대한 경로의 리스트를 오름차순으로 정리
        
        os.mkdir('%s/%s' %(output_path,pidx[e])) # path2에 pid명으로 폴더 생성
        
        file_in = [] # 길이내에 더할 파일
        df_new = pd.DataFrame() # df를 합치고 모을 DataFrame 
                
        for h in tqdm(range(0,len(pidpath)),desc='PID:%s인 csv파일 df_new에 저장' %(pidx[e])): # 분류된 한 pid의 길이 확인     
            df = pd.read_csv(pidpath[h], names = ['1', '2', '3']) 
            # 칼럼이 늘어나는 것을 방지/csv파일을 df으로 바꾸기                
            df_new = pd.concat([df_new, df]) # df를 df_new에 더하고 길이가 24시간 이하
            file_in.append(os.path.basename(str(pidpath[h]))[:-4] + '\n')
              
        num_of_file_in_day = 86400 # 24시간 x 500Hz
        df_day = df_new/(num_of_file_in_day)
        print(len(df_new,df_day))
        
        for j in tqdm(range(0,len(df_day)),desc='PID:%s인 df_new %s개로 분할' %(pidx[e],(len(df_day)+1))):
            # pid 24시간마다 분할
            if j == 0:
                globals()['df_new_%d' %j] = df_new.iloc[0:(num_of_file_in_day),:] 
                # 데이터 프레임 행 나누기 [시작행:끝행(미포함),시작열:끝열(미포함)]
            elif j == len(df_new/num_of_file_in_day): 
                # 마지막 사이클에서는 24시간으로 자르고 남은 데이터도 모으기
                globals()['df_new_%d' %j] = df_new.iloc[(num_of_file_in_day)*j+1:(num_of_file_in_day)*(j+2),:]
                globals()['df_new_%d' %(j+1)] = df_new.iloc[(num_of_file_in_day)*(j+2):,:]
            else: # ㄱ
                globals()['df_new_%d' %j] = df_new.iloc[(num_of_file_in_day)*j+1:(num_of_file_in_day)*(j+2),:]
            
            
        st0 = dt.datetime.now() # txt 생성시작시간
        print('총 %s중 %s번째 txt 생성 ' %(len(pidx),e+1)) # txt파일 생성 시작           
        with open('%s/%s/%s.txt' %(output_path,pidx[e],pidx[e]), 'w') as f: # paht2/pid 경로에 pid명으로 txt생성
            f.writelines(file_in) # 생성한 pid.txt에 이어붙인 파일 목록을 넣어라
        et0 = dt.datetime.now()
        dt0 = et0 - st0
        print('완료 / 걸린시간 =',dt0) # 완료 / 걸린시간 확인
        
        st1 = dt.datetime.now()    
        print('%s번째 csv파일 생성 ' %(e+1), end=' ') # csv파일 생성 확인
        df_new.to_csv('%s/%s/%s.csv' %(output_path,pidx[e],pidx[e]), index = False, header = None)
        # path2/pid폴더에 pid명으로 csv 파일을 만들자, 인덱스없이, 내용을 columns으로 만들지 않는다
        et1 = dt.datetime.now()
        dt1 = et1 - st1
        print('완료 / 걸린시간 =', dt1) # 완료 / 걸린시간 확인


    
    
    
    