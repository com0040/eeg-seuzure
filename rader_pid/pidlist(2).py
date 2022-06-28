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

def pidlist(path1,path2):   
    
    filePath = '%s' %(path1)  # 폴더 주소를 path1으로 받아서 저장
    fileall = os.listdir(filePath) # 경로내에 있는 파일모두 불러서 리스트화
    fileCsv = [filePath + f[:-4] for f in fileall if f.endswith('.csv')] # csv에만 적용해라 f=0번째
    CSVname =[] # 전체 CSV파일이름 리스트로 저장용
    CSVname.append(os.path.basename(fileCsv)) # 파일 이름만 CSVname에 리스트로 저장
    listpid =[] # 전체 pid 리스트로 저장용
    
    print(fileall)
    for i in range (0,len(fileCsv)): # 불러온 CSV파일의 수만큼 반복
        print()
        CSVname.append(os.path.basename(str(fileCsv[i]))) # 파일 이름만 CSVname에 리스트로 저장
        splitCSV = CSVname[i].split("_") # 파일 이름을 분할 [0]에 pid 저장 / [1] 시작시간 저장
        listpid.append(splitCSV[0]) # listpid에 pid만 리스트로 저장

        pidx = list(set(listpid)) # pid중 중복되는 것 제거
    
    print('pid 중복제거 끝/총 파일 수='+str(i+1)) # 제거확인
    for e in range (0,len(pidx)): # 중복되지 않은 pid만큼 반복
        print('%s번째 PID:%s 분류 시작' %((e+1),pidx[e])) # 시작 확인
        pidpath =[] # 같은 pid경로를 리스트로 저장
        for j in range (0,len(CSVname)): # 같은 pid를 찾기 위해 CSVname의 길이만큼 반복
            if pidx[e] == listpid[j]: 
                # pidx에서 e번째 pid와 CSVsplit(CSVname의 j번째) pid와 같은지 확인                         
                pidpath.append(filePath + '%s' %(CSVname[j]) + '.csv' )
                # 같다면 pidpath에 pid와 시작시간을 포함한 CSVname의 j번째 파일 경로를 저장    
        pidpath.sort() # 한 pid에 대한 경로의 리스트를 오름차순으로 정리
       
        df_total = 0 # df의 길이를 더해줄 변수/매pid마다 길이 늘임 방지
        df_time = 0 # 매pid마다 길이 늘임 방지를 위해 df_time의 길이를 초기화
        print('%s번째 분류 끝 ' %str(e+1)) # 분류 확인
        
        file_in = [] # 길이내에 더할 파일
        df_new = pd.DataFrame() # df를 합치고 모을 DataFrame 
        
        for h in range(0,len(pidpath)): # 분류된 한 pid의 길이 확인
            if df_time <= 86400: # 한 pid의 측정시간이
                # 하루 = 24(h)*60(min)*60(sec) = 86400 보다 작을때만 진행                 
                df_length = int() # 불러올 csv파일의 길이 확인용/초기화
                df = pd.read_csv(pidpath[h], names = ['1', '2', '3']) 
                # 칼럼이 늘어나는 것을 방지/csv파일을 df으로 바꾸기
                df_length = len(df) # df의 길이를 df_length로 넣어준다
                df_total = (df_total + df_length) # 한 pid에 대한 관련 csv파일의 길이를 다 더한다
                df_time = df_total / 500 # 다 더한 값을 sample rate로 나누어서 초로 변환
                df_new = pd.concat([df_new, df]) # df를 df_new에 더하고 길이가 24시간 이하
                file_in.append(os.path.basename(str(pidpath[h]))[:-4] + '\n')
                # 사용된 파일들을 리스트로 만들기 + 엔터                
            else: # 24시간보다 커지면 24시간 보다 작은 값을 가지고
                break # for문을 끝냄
            
        os.mkdir('%s%s' %(path2,pidx[e])) # path2에 pid명으로 폴더 생성
        
        with open('%s%s/%s.txt' %(path2,pidx[e],pidx[e]), 'w') as f: # paht2/pid 경로에 pid명으로 txt생성
            f.writelines(file_in) # 생성한 pid.txt에 이어붙인 파일 목록을 넣어라
                
        print('%s번째 csv파일 생성' %(e+1)) # csv파일 생성 확인
        df_new.to_csv('%s%s/%s.csv' %(path2,pidx[e],pidx[e]), index = False, header = None)
        # path2/pid폴더에 pid명으로 csv 파일을 만들자, 인덱스없이, 내용을 columns으로 만들지 않는다
