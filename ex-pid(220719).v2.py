# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 15:44:07 2022

@author: chang
"""
import os # 파일을 복사하거나 디렉터리를 생성하고 특정 디렉터리 내의 파일 목록 구하기
import csv
import pandas as pd # 행과 열로 구성된 객체 생성, 안정적 데이터 처리
 # import matplotlib.pyplot as plt # 시각화 패키지
import numpy as np # 고성능 과학 계산용 패키지
# import natsort
import sys
from pandas import DataFrame
import datetime as dt
# from pidlist import pidlist # pidlist 파일에서 함수 전부 가져오기
from tqdm import tqdm
from datetime import datetime, timedelta
import time
#'//192.168.45.194/Data/CCU_databa10/'
# C:\Users\chang\Desktop\CCU_databa10(concat)          
 
input_path = '//192.168.45.194/Data/CCU_databa10/'   # 폴더 주소를 입력 
output_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/CCU_databa10(concat)/'
   
st3 = dt.datetime.now() 
print('시작시간', st3, end = ' ')
fileall = os.listdir(input_path) # 경로내에 있는 파일모두 불러서 리스트화
fileCsv = [input_path + f[:-4] for f in fileall if f.endswith('.csv')] # csv에만 적용해라 f=0번째
filename_csv =[f[:-4] for f in fileall if f.endswith('.csv')]            
et3 = dt.datetime.now()
dt = et3-st3
print('파일 로드 끝', dt)
st2 = dt.datetime.now() 
splitCSV = [filename_csv[i].split("_") for i in range(0,len(filename_csv))] 
# 파일 이름을 분할 [0]에 pid 저장 / [1] 시작시간 저장

pid = [splitCSV[i][0] for i in range(0,len(filename_csv))]

pid_without_overrap = list(set(pid)) # pid중 중복되는 것 제거
# pid_without_overrap.sort(reverse=True) 

filename='CCU_databa(0)' #파일명 고정값     

uniq=1 # 파일명에 추가할 숫자
while os.path.exists(output_path):  #동일한 파일명이 존재할 때
  output_path='//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/CCU_databa10(concat)/%s(%d)' % (
      filename[:-3],uniq) #파일명(1) 파일명(2)...
  uniq+=1 # 반복되면서 숫자 증가

os.mkdir('%s' %(output_path)) 
# 파일명도 저장되어 있는 output_path로 폴더생성/이후에 저장될 경로이기도 함

et2 = dt.datetime.now() # 현재시간
dt2 = et2 - st2 # 걸린 시간
print('파일읽고 폴더생성 완료 걸린시간', dt2) # 걸린시간 확인 밑 잘 구동되는지 확인
pid_list_in_csv_txtfile = [] # pid_without_overrap에 포함되는 pidpath안에 pid를 더해 text 파일화
num_of_file_in_day = 86400*500

i=1
for e in range (0,len(pid_without_overrap)):
    print('중복없는 총 %s개의 pid 중 같은 pid를 한 list로 %s번째 합치기' %(len(pid_without_overrap),i)) # 중복되지 않은 pid만큼 반복
    i+=1
    pidpath =[input_path + '%s' %(filename_csv[f]) + '.csv' for f in range(
        0,len(pid)) if pid_without_overrap[e] == pid[f]] 
    # 같은 pid경로를 리스트로 저장     
    pidpath.sort() # 한 pid에 대한 경로의 리스트를 오름차순으로 정리
    
    os.mkdir('%s/%s' %(output_path,pid_without_overrap[e])) # path2에 pid명으로 폴더 생성
             
    df_new = pd.DataFrame() # df를 합치고 모을 DataFrame 
        
    j=1
    for h in tqdm(range(0,len(pidpath)),desc='PID : %s인 csv 파일 df_new에 저장' %(pid_without_overrap[e])): # 분류된 한 pid의 길이 확인     
        if h!=0:  
            day_format =  "%Y%m%d%H%M%S.%f" # 시간을 담기위한 포멧
            compare_day_1 = pidpath[h-1][44:58] # 시간에 해당하는 부분을 가져온다 1
            compare_day_2 = pidpath[h][44:58] # 시간에 해당하는 부분을 가져온다 2
            trans_day_1 = datetime.strptime(compare_day_1, day_format) # 문자열을 시간으로 만든다 1
            trans_day_2 = datetime.strptime(compare_day_2, day_format) # 문자열을 시간으로 만든다 2
            
            time_dif = trans_day_2 - trans_day_1 # 시간차이를 구해준다.
            add_dif = time_dif + timedelta(hours=0) # 시간차이를 더해준다
            
            if add_dif >= timedelta(days=1): # 더하다가 1일이 넘으는 경우 
# 1.연속될 수도 있고 아닐수도 있지만 자료들의 시간 차이가 처음 기록된 시간에서 하루가 지나지않도록 함
# 2.24시간은 되지 않았지만 날짜가 바뀌어 더해준 시간이 급하게 증가된 경우
                df_new.to_csv('%s/%s/%s(%s).csv' %(output_path,pid_without_overrap[e],
                            pid_without_overrap[e],j), index = False, header = None)
            # csv 파일 만들고
                df_new = pd.DataFrame() # 초기화 
                df = pd.read_csv(pidpath[h], names = ['1', '2', '3']) 
    # 칼럼이 늘어나는 것을 방지/csv파일을 df으로 바꾸기                
    # csv가 만들어지지만 h-1까지 만들어지므로 h를 다시 새로운 df_new에 넣어줌
                df_new = pd.concat([df_new, df]) # df를 그냥 합치면서 list에 저장 후
                pid_list_in_csv_txtfile.append(os.path.basename(str(pidpath[h]))[:-4] + '\n')
                add_dif = timedelta(days=0) # 더해준 시간 초기화
            elif add_dif <= timedelta(days=1):
                # 차이를 계속 더하는데 1일미만일때만 df만들어서 더함
                df = pd.read_csv(pidpath[h], names = ['1', '2', '3']) 
    # 칼럼이 늘어나는 것을 방지/csv파일을 df으로 바꾸기                
                df_new = pd.concat([df_new, df]) # df를 그냥 합치면서 list에 저장 후
                pid_list_in_csv_txtfile.append(os.path.basename(str(pidpath[h]))[:-4] + '\n')
            
            elif h==(len(pidpath)-1):
                df_new.to_csv('%s/%s/%s(%s).csv' %(output_path,pid_without_overrap[e],
                          pid_without_overrap[e],j), index = False, header = None)
    # 마지막일 경우 csv 파일 만들고 사이클 종료

    print('총 %s중 %s번째 txt ' %(len(pid_without_overrap),e+1), end = ' ') # txt파일 생성 시작           
    with open('%s/%s/%s.txt' %(output_path,pid_without_overrap[e],pid_without_overrap[e]), 'w'
              ) as f: # paht2/pid 경로에 pid명으로 txt생성
        f.writelines(pid_list_in_csv_txtfile) # 생성한 pid.txt에 이어붙인 파일 목록을 넣어라
         
    del pidpath# 변수 데이터 삭제
    # pid경로를 불러서 df_new와 text로 만드는 함수 호출               
    
