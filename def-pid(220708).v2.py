# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 16:51:04 2022

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

# def one_day_df_to_csv(day_data,num_of_file_in_day,df_new,pid_without_overrap,output_path,e):
#     for j in tqdm(range(0,day_data),desc='PID:%s인 df_new %s개로 분할' %(pid_without_overrap[e],(day_data)+1)):
#         # pid 24시간마다 분할 /day_data가 1일때 마지막 반복이므로 첫if문에 먼저 넣어준다       
#         if j == (day_data-1): # 0 부터 시작하기 때문에 1을 빼서 마지막으로 맞춤
#             # 마지막 사이클에서는 24시간으로 자르고 남은 데이터 모아서 cvs로
#             locals()['df_new_%d' %j] = df_new.iloc[(num_of_file_in_day*j)+1:(num_of_file_in_day)*(j+1),:]
#             locals()['df_new_%d' %j].to_csv('%s/%s/%s(%s).csv' %(output_path,pid_without_overrap[e],pid_without_overrap[e],j), index = False, header = None)
#             del locals()['df_new_%d' %j] # 동적변수 초기화
            
#             locals()['df_new_%d' %(j+1)] = df_new.iloc[(num_of_file_in_day)*(j+1):,:]
#             locals()['df_new_%d' %(j+1)].to_csv('%s/%s/%s(%s).csv' %(output_path,pid_without_overrap[e],pid_without_overrap[e],j+1), index = False, header = None)
#             del locals()['df_new_%d' %(j+1)]
#         elif j == 0: # 동적 변수 선언해서 분할후에 df만들어 csv로 만들기        
#             locals()['df_new_%d' %j] = df_new.iloc[0:num_of_file_in_day,:]
#             locals()['df_new_%d' %j].to_csv('%s/%s/%s(%s).csv' %(output_path,pid_without_overrap[e],pid_without_overrap[e],j), index = False, header = None)
#             # 데이터 프레임 행 나누기 [시작행:끝행(미포함),시작열:끝열(미포함)]
#             del locals()['df_new_%d' %j]
#         else: # 중간 사이클     
#             locals()['df_new_%d' %j] = df_new.iloc[(num_of_file_in_day)*j+1:(num_of_file_in_day)*(j+1),:]
#             locals()['df_new_%d' %j].to_csv('%s/%s/%s(%s).csv' %(output_path,pid_without_overrap[e],pid_without_overrap[e],j), index = False, header = None)
#             # df_new로 시작하는 동적 변수를 만들어 
#             del locals()['df_new_%d' %j] # 동적변수 초기화
#     del df_new
            
def load_csv_by_path(input_path,output_path): # 경로에 있는 csv불러오기
    st3 = dt.datetime.now() 
    print('시작시간', st3, end = ' ')
    fileall = os.listdir(input_path) # 경로내에 있는 파일모두 불러서 리스트화    
    filename_csv =[f[:-4] for f in fileall if f.endswith('.csv')] # csv파일만 가져오기
    print('파일 로드 끝')
    splitCSV = [filename_csv[i].split("_") for i in range(0,len(filename_csv))] 
    # 파일 이름을 분할 [0]에 pid 저장 / [1] 시작시간 저장
    pid = [splitCSV[i][0] for i in range(0,len(splitCSV))]
    
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
    
    et3 = dt.datetime.now() # 현재시간
    dt3 = et3 - st3 # 걸린 시간
    print('파일읽고 폴더생성 완료 걸린시간', dt3) # 걸린시간 확인 밑 잘 구동되는지 확인
    
    return pid,filename_csv,output_path, input_path, pid_without_overrap
    # 내보낼 변수 
    
def load_pidpath_write_df_new_pid_text(pidpath,output_path,pid_without_overrap,e):
    df_new = pd.DataFrame() # df를 합치고 모을 DataFrame 
    pid_list_in_csv_txtfile = [] # pid_without_overrap에 포함되는 pidpath안에 pid를 더해 text 파일화
    num_of_file_in_day = 86400*500
    j=1
    for h in tqdm(range(0,len(pidpath)),desc='PID : %s인 csv 파일 df_new에 저장' %(pid_without_overrap[e])): # 분류된 한 pid의 길이 확인     
        df = pd.read_csv(pidpath[h], names = ['1', '2', '3']) 
        # 칼럼이 늘어나는 것을 방지/csv파일을 df으로 바꾸기                
        df_new = pd.concat([df_new, df]) # df를 그냥 합치면서 list에 저장 후
        pid_list_in_csv_txtfile.append(os.path.basename(str(pidpath[h]))[:-4] + '\n')
        # 해당하는 pid 리스트를 txt에 저장
        if len(df_new)/num_of_file_in_day ==1:
            # df_new가 길어지는 것을 방지하기 위해 하루치가 되었을 경우
            df_divide_1 = df_new.iloc[:num_of_file_in_day,:] # 하루의 데이터량만큼 자르고
            df_divide_1.to_csv('%s/%s/%s(%s).csv' %(output_path,pid_without_overrap[e],
                                               pid_without_overrap[e],j), index = False, header = None)
            # 바로 csv파일로 만들어준다
            df_new = pd.DataFrame() # 남은 데이터를 저장하기 위해 비워주고
            df_divide_2 = df_new.iloc[num_of_file_in_day:,:] # 자르고 남은 데이터를
            df_new = pd.concat([df_new, df_divide_2]) # 넣어준다
            j+=1 # 같은 환자의 몇 일째인지 증가 표시
            del df_divide_1, df_divide_2
        elif h == len(pidpath)-1: # 24시간이 안되는 경우가 마지막일 것이니까
            df_new.to_csv('%s/%s/%s(%s)less_24h.csv' %(output_path,pid_without_overrap[e],
                                               pid_without_overrap[e],j), index = False, header = None)
            
            del df_new
        del df 
        
    print('총 %s중 %s번째 txt ' %(len(pid_without_overrap),e+1), end = ' ') # txt파일 생성 시작           
    with open('%s/%s/%s.txt' %(output_path,pid_without_overrap[e],pid_without_overrap[e]), 'w') as f: # paht2/pid 경로에 pid명으로 txt생성
        f.writelines(pid_list_in_csv_txtfile) # 생성한 pid.txt에 이어붙인 파일 목록을 넣어라
         
    del pidpath, pid_without_overrap # 변수 데이터 삭제
    # return df_new, pid_list_in_csv_txtfile # 꺼낼 변수

def repeat_pid_without_overrap_length():
    input_path = '//192.168.45.194/Data/CCU_databa10/'   # 폴더 주소를 입력 
    output_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/CCU_databa10(concat)/'
    pid,filename_csv,output_path, input_path,pid_without_overrap = load_csv_by_path(input_path, output_path)
    i=1
    for e in range (0,len(pid_without_overrap)):
        print('중복없는 총 %s개의 pid 중 같은 pid를 한 list로 %s번째 합치기' %(len(pid_without_overrap),i)) # 중복되지 않은 pid만큼 반복
        i+=1
        pidpath =[input_path + '%s' %(filename_csv[f]) + '.csv' for f in range(
            0,len(pid)) if pid_without_overrap[e] == pid[f]] 
        # 같은 pid경로를 리스트로 저장     
        pidpath.sort() # 한 pid에 대한 경로의 리스트를 오름차순으로 정리
        
        os.mkdir('%s/%s' %(output_path,pid_without_overrap[e])) # path2에 pid명으로 폴더 생성
                 
        df_new, pid_list_in_csv_txtfile = load_pidpath_write_df_new_pid_text(output_path,pidpath, pid_without_overrap,e)
        # pid경로를 불러서 df_new와 text로 만드는 함수 호출               
        # num_of_file_in_day = 86400*500 # 24시간 x 500Hz
        # day_data = int(len(df_new)/(num_of_file_in_day)) # 한 pid로 만든 df의 길이를 하루
        # print(len(df_new))       # print(day_data)        
        # if day_data !=0:
        #     # df의 길이가 하루 이상일 경우            
        #     one_day_df_to_csv(day_data, num_of_file_in_day, df_new, pid_without_overrap, output_path,e)
                    
        #     print('총 %s중 %s번째 txt ' %(len(pid_without_overrap),e+1), end = ' ') # txt파일 생성 시작           
        #     with open('%s/%s/%s.txt' %(output_path,pid_without_overrap[e],pid_without_overrap[e]), 'w') as f: # paht2/pid 경로에 pid명으로 txt생성
        #         f.writelines(pid_list_in_csv_txtfile) # 생성한 pid.txt에 이어붙인 파일 목록을 넣어라
                
        # else:
        #     print('하루미달 -->', end=' ')
                  
        #     print('총 %s중 %s번째 txt ' %(len(pid_without_overrap),e+1), end = ' ') # txt파일 생성 시작           
        #     with open('%s/%s/%s.txt' %(output_path,pid_without_overrap[e],pid_without_overrap[e]), 'w') as f: # paht2/pid 경로에 pid명으로 txt생성
        #         f.writelines(pid_list_in_csv_txtfile) # 생성한 pid.txt에 이어붙인 파일 목록을 넣어라
                   
        #     st1 = dt.datetime.now()    
        #     print('csv 파일 생성 ', end=' ') # csv파일 생성 확인
        #     df_new.to_csv('%s/%s/%s.csv' %(output_path,pid_without_overrap[e],pid_without_overrap[e]), index = False, header = None)
        #     # path2/pid폴더에 pid명으로 csv 파일을 만들자, 인덱스없이, 내용을 columns으로 만들지 않는다
        #     et1 = dt.datetime.now()
        #     dt1 = et1 - st1
        #     print('완료 / 걸린시간 =', dt1, end='/n/n') # 완료 / 걸린시간 확인
        del df_new, pid_list_in_csv_txtfile, pidpath
        
''' locals()['pid_list_in_csv_txtfile_%d' %j] = pid_list_in_csv_txtfile[0:day_data]
with open('%s/%s/%s%s.txt' %(output_path,pid_without_overrap[e],pid_without_overrap[e],j), 'w') as f: # paht2/pid 경로에 pid명으로 txt생성
    f.writelines(locals()['pid_list_in_csv_txtfile_%d' %j]) # 생성한 pid.txt에 이어붙인 파일 목록을 넣어라 '''
repeat_pid_without_overrap_length()
