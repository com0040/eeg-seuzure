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
    
    foldername = 'CCU_databa'
    filePath = '%s' %(path1)  # 폴더 주소를 path1으로 받아서 저장
    fileall = os.listdir(filePath) # 경로내에 있는 파일모두 불러서 리스트화    
    filename_csv =[f[:-4] for f in fileall if f.endswith('.csv')] # csv파일만 가져오기
    splitCSV = [filename_csv[i].split("_") for i in range(0,len(filename_csv))] # 파일 이름을 분할 [0]에 pid 저장 / [1] 시작시간 저장
    pid = [splitCSV[i][0] for i in range(0,len(splitCSV))]
    
    pidx = list(set(pid)) # pid중 중복되는 것 제거

    print('pid 중복제거 끝/총 파일 수= %d' % len(pidx)) # 제거확인
    i=1
    for e in tqdm(range (0,len(pidx))
                  ,desc='중복없는 총 %s개의 pid 중 같은 pid를 한 list로 %s번째 합치기' %(len(pidx),i)): # 중복되지 않은 pid만큼 반복
        # st2 = dt.datetime.now()
        # print('\n총 %s개 PID 중 %s번째 PID:%s 분류 시작' %(len(pidx),(e+1),pidx[e])) # 시작 확인
        i+=1
        pidpath =[filePath + '%s' %(filename_csv[f]) + '.csv' for f in range(0,len(pid)) if pidx[e] == pid[f]] 
        # 같은 pid경로를 리스트로 저장     
        pidpath.sort() # 한 pid에 대한 경로의 리스트를 오름차순으로 정리
       
        df_total = 0 # df의 길이를 더해줄 변수/매pid마다 길이 늘임 방지
        df_time = 0 # 매pid마다 길이 늘임 방지를 위해 df_time의 길이를 초기화
        '''et2 = dt.datetime.now()
        dt2 = et2 -st2
        # print('분류 끝-길이확인 시작 / 걸린시간 : %s,' %(dt2)) # 분류 확인
        '''
        os.mkdir('%s%s' %(path2,pidx[e])) # path2에 pid명으로 폴더 생성
        
        file_in = [] # 길이내에 더할 파일
        df_new = pd.DataFrame() # df를 합치고 모을 DataFrame 
                
        for h in tqdm(range(0,len(pidpath)),desc='PID:%s인 csv파일 총 %s개 df_new에 저장' %(pidx[e],len(pidpath))): # 분류된 한 pid의 길이 확인     
            # st2 = dt.datetime.now()
            # df_length = int() # 불러올 csv파일의 길이 확인용/초기화
            df = pd.read_csv(pidpath[h], names = ['1', '2', '3']) 
            # 칼럼이 늘어나는 것을 방지/csv파일을 df으로 바꾸기
            # df_length = len(df) # df의 길이를 df_length로 넣어준다
            # df_total = (df_total + df_length) # 한 pid에 대한 관련 csv파일의 길이를 다 더한다
            # df_time = df_total / 500 # 다 더한 값을 sample rate로 나누어서 초로 변환
            
            splitCSV
          
            # 사용된 파일들을 리스트로 만들기 + 엔터                
            if df_time <= 86400: # 한 pid의 측정시간이   
                # 하루 = 24(h)*60(min)*60(sec) = 86400 보다 작을때만 진행    
                df_new = pd.concat([df_new, df]) # df를 df_new에 더하고 길이가 24시간 이하
                file_in.append(os.path.basename(str(pidpath[h]))[:-4] + '\n')
                print('df_new 생성중 총 %s개 중 %s개 완료' %(len(pidpath),h+1))
            else : # 24시간보다 커지면 24시간 보다 작은 값을 가지고
                print('24시간 초과') # 24시간 초과시
                file_in = [] # txt로만들 리스트 초기화
                # break # for문을 끝냄  
                    
        st0 = dt.datetime.now() # txt 생성시작시간
        print('총 %s중 %s번째 txt 생성 ' %(len(pidx),e+1)) # txt파일 생성 시작           
        with open('%s%s/%s.txt' %(path2,pidx[e],pidx[e]), 'w') as f: # paht2/pid 경로에 pid명으로 txt생성
            f.writelines(file_in) # 생성한 pid.txt에 이어붙인 파일 목록을 넣어라
        et0 = dt.datetime.now()
        dt0 = et0 - st0
        print('완료 / 걸린시간 =',dt0) # 완료 / 걸린시간 확인
        
        st1 = dt.datetime.now()    
        print('%s번째 csv파일 생성 ' %(e+1), end=' ') # csv파일 생성 확인
        df_new.to_csv('%s%s/%s.csv' %(path2,pidx[e],pidx[e]), index = False, header = None)
        # path2/pid폴더에 pid명으로 csv 파일을 만들자, 인덱스없이, 내용을 columns으로 만들지 않는다
        et1 = dt.datetime.now()
        dt1 = et1 - st1
        print('완료 / 걸린시간 =', dt1) # 완료 / 걸린시간 확인


    
    
    
    