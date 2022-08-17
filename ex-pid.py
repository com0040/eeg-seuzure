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
from tqdm import tqdm
#'//192.168.45.194/Data/CCU_databa10/'
# C:\Users\chang\Desktop\CCU_databa10(concat)
st3 = dt.datetime.now() 
print('시작시간', st3, end = ' ')
path2 = 'C:/Users/chang/Desktop/CCU_databa10(concat)/'

filePath = '//192.168.45.194/Data/CCU_databa10/'   # 폴더 주소를 입력
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

et3 = dt.datetime.now() 
dt3 = et3 - st3
print('파일읽고 폴더생성 완료시간', et3, '걸린시간', dt3)
i=1
for e in range (0,len(pidx)):
    print('중복없는 총 %s개의 pid 중 같은 pid를 한 list로 %s번째 합치기' %(len(pidx),i)) # 중복되지 않은 pid만큼 반복
    i+=1
    pidpath =[filePath + '%s' %(filename_csv[f]) + '.csv' for f in range(0,len(pid)) if pidx[e] == pid[f]] 
    # 같은 pid경로를 리스트로 저장     
    pidpath.sort() # 한 pid에 대한 경로의 리스트를 오름차순으로 정리
    
    os.mkdir('%s/%s' %(output_path,pidx[e])) # path2에 pid명으로 폴더 생성
    
    pid_list_in_csv_txtfile = [] # 길이내에 더할 파일
    df_new = pd.DataFrame() # df를 합치고 모을 DataFrame 
            
    for h in tqdm(range(0,len(pidpath)),desc='PID : %s인 csv 파일 df_new에 저장' %(pidx[e])): # 분류된 한 pid의 길이 확인     
        df = pd.read_csv(pidpath[h], names = ['1', '2', '3']) 
        # 칼럼이 늘어나는 것을 방지/csv파일을 df으로 바꾸기                
        df_new = pd.concat([df_new, df]) # df를 df_new에 더하고 길이가 24시간 이하
        pid_list_in_csv_txtfile.append(os.path.basename(str(pidpath[h]))[:-4] + '\n')
          
    num_of_file_in_day = 86400*500 # 24시간 x 500Hz
    day_data = int(len(df_new)/(num_of_file_in_day)) # 한 pid로 만든 df의 길이를 하루
    # print(len(df_new))
    # print(day_data)
    
    if day_data !=0:
    
        for j in tqdm(range(0,day_data),desc='PID:%s인 df_new %s개로 분할' %(pidx[e],(day_data)+1)):
            # pid 24시간마다 분할
            if j == 0: # 동적 변수 선언해서 분할후에 df만들어 csv로 만들기
            
                
                    
                locals()['df_new_%d' %j] = df_new.iloc[0:day_data,:]
                locals()['df_new_%d' %j].to_csv('%s/%s/%s%s.csv' %(output_path,pidx[e],pidx[e],j), index = False, header = None)
                # 데이터 프레임 행 나누기 [시작행:끝행(미포함),시작열:끝열(미포함)]
            elif j == (day_data-1): # 0 부터 시작하기 때문에 1을 빼서 마지막으로 맞춤
                # 마지막 사이클에서는 24시간으로 자르고 남은 데이터 모아서 cvs로
                
                locals()['pid_list_in_csv_txtfile_%d' %j] = pid_list_in_csv_txtfile[(day_data)*j+1:(day_data)*(j+1)]
                with open('%s/%s/%s%s.txt' %(output_path,pidx[e],pidx[e],j), 'w') as f: # paht2/pid 경로에 pid명으로 txt생성
                    f.writelines(locals()['pid_list_in_csv_txtfile_%d' %j]) # 생성한 pid.txt에 이어붙인 파일 목록을 넣어라
                locals()['pid_list_in_csv_txtfile_%d' %j]=0 # 동적변수 초기화
                
                locals()['df_new_%d' %j] = df_new.iloc[(day_data)*j+1:(day_data)*(j+1),:]
                locals()['df_new_%d' %j].to_csv('%s/%s/%s%s.csv' %(output_path,pidx[e],pidx[e],j), index = False, header = None)
                locals()['df_new_%d' %j]=0 # 동적변수 초기화
                
                locals()['pid_list_in_csv_txtfile_%d' %(j+1)] = pid_list_in_csv_txtfile[(day_data)*j+1:]
                with open('%s/%s/%s%s.txt' %(output_path,pidx[e],pidx[e],j+1), 'w') as f: # paht2/pid 경로에 pid명으로 txt생성
                    f.writelines(locals()['pid_list_in_csv_txtfile_%d' %j]) # 생성한 pid.txt에 이어붙인 파일 목록을 넣어라
                locals()['pid_list_in_csv_txtfile_%d' %j+1]=0 # 동적변수 초기화
                
                locals()['df_new_%d' %(j+1)] = df_new.iloc[(day_data)*(j+1):,:]
                locals()['df_new_%d' %j].to_csv('%s/%s/%s%s.csv' %(output_path,pidx[e],pidx[e],j+1), index = False, header = None)
                locals()['df_new_%d' %(j+1)]=0
            else: # 중간 사이클     
                locals()['df_new_%d' %j] = df_new.iloc[(day_data)*j+1:(day_data)*(j+1),:]
                locals()['df_new_%d' %j].to_csv('%s/%s/%s%s.csv' %(output_path,pidx[e],pidx[e],j), index = False, header = None)
                # df_new로 시작하는 동적 변수를 만들어 
                del locals()['df_new_%d' %j] # 동적변수 초기화
                
        print('총 %s중 %s번째 txt ' %(len(pidx),e+1), end = ' ') # txt파일 생성 시작           
        with open('%s/%s/%s.txt' %(output_path,pidx[e],pidx[e]), 'w') as f: # paht2/pid 경로에 pid명으로 txt생성
            f.writelines(pid_list_in_csv_txtfile) # 생성한 pid.txt에 이어붙인 파일 목록을 넣어라
            
    else:
        print('하루미달 -->', end=' ')
        
        #st0 = dt.datetime.now() # txt 생성시작시간
        print('총 %s중 %s번째 txt ' %(len(pidx),e+1), end = ' ') # txt파일 생성 시작           
        with open('%s/%s/%s.txt' %(output_path,pidx[e],pidx[e]), 'w') as f: # paht2/pid 경로에 pid명으로 txt생성
            f.writelines(pid_list_in_csv_txtfile) # 생성한 pid.txt에 이어붙인 파일 목록을 넣어라
        # et0 = dt.datetime.now()
        # dt0 = et0 - st0
        # print('완료 / 걸린시간 =',dt0) # 완료 / 걸린시간 확인
        
        st1 = dt.datetime.now()    
        print('csv 파일 생성 ', end=' ') # csv파일 생성 확인
        df_new.to_csv('%s/%s/%s.csv' %(output_path,pidx[e],pidx[e]), index = False, header = None)
        # path2/pid폴더에 pid명으로 csv 파일을 만들자, 인덱스없이, 내용을 columns으로 만들지 않는다
        et1 = dt.datetime.now()
        dt1 = et1 - st1
        print('완료 / 걸린시간 =', dt1, end='/n/n') # 완료 / 걸린시간 확인
        
        locals()['pid_list_in_csv_txtfile_%d' %j] = pid_list_in_csv_txtfile[0:day_data]
        with open('%s/%s/%s%s.txt' %(output_path,pidx[e],pidx[e],j), 'w') as f: # paht2/pid 경로에 pid명으로 txt생성
            f.writelines(locals()['pid_list_in_csv_txtfile_%d' %j]) # 생성한 pid.txt에 이어붙인 파일 목록을 넣어라