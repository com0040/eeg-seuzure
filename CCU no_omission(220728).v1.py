# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 12:38:01 2022

@author: chang
"""
import math
import string
import glob
import re
import os # 파일을 복사하거나 디렉터리를 생성하고 특정 디렉터리 내의 파일 목록 구하기
import csv
import pandas as pd # 행과 열로 구성된 객체 생성, 안정적 데이터 처리
import matplotlib.pyplot as plt # 시각화 패키지
import numpy as np # 고성능 과학 계산용 패키지
from numpy import *
import natsort
import sys
from pandas import DataFrame
import datetime as dt # from pidlist import pidlist # pidlist 파일에서 함수 전부 가져오기
from tqdm import tqdm
import pyedflib

input_path ='//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/CCU_databa10(concat)/CCU_databa(0) - txt-omission/'
output_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/CCU_databa10(concat)/CCU_no_omission/'

file_path_list = []
file_name_list = []
file_label = []
st3 = dt.datetime.now()
print('시작시간', st3, end = ' ')
for (root, directories, files) in os.walk(input_path):
    # 경로를 3가지로 분리해서 가져옴/root:폴더 경로/files:파일명
    for file in (files): # files에서
        if file.endswith('.csv'): # .csv 확장자 인거만 가져와서
            file_name = file[:-4]
            file_path = os.path.join(root, file)
            # 경로와 파일명 합쳐서 file_path에 합쳐주고 누적은 안되니
            file_name_list.append(file_name)
            file_path_list.append(file_path)
            # 만들때 마다 리스트에 저장하자
        elif file.endswith('.txt'): # 라벨들어있는 txt
            file_path = os.path.join(root, file) # 경로를 따서
            file_label.append(file_path) # 따로 저장
print('파일 로드 끝')

splitCSV = [file_name_list[i].split("_") for i in range(0,len(file_name_list))]
# 파일 이름을 분할 [0]에 pid 저장 / [1] 시작시간 저장
pid = [file_name_list[i][:8] for i in range(0,len(file_name_list))]
# 분리된 것 중 pid만 저장
pid_without_overrap = list(set(pid)) # pid중 중복되는 것 제거
# 이미 생성된 csv이므로 (0)같이 주기가 되있으므로
# pid[:-3] = 0-(뒤에서 3개를 뺀곳 까지) 불러오기

for e in range (0,len(pid_without_overrap)):
    print('총 %s 중 %s번째 생성시작' %(len(pid_without_overrap),e), end=' ')
    
    if os.path.exists('%s/%s' %(output_path,pid_without_overrap[e])):
        if len(os.listdir('%s%s' %(output_path,pid_without_overrap[e]))) == 0:
            print('있는데 비어서 재생성을 위해 삭제')
            os.rmdir('%s%s' %(output_path,pid_without_overrap[e]))
        else:
            print('있는 파일 생략!')
        continue
    # 혹시 이미 만들어진 pid라고 판단되면 아래코드 무시
    
    os.mkdir('%s%s' %(output_path,pid_without_overrap[e])) # path2에 pid명으로 폴더 생성
    
    pidpath = ['%s' %(file_path_list[f]) for f in range(
        0,len(pid)) if pid_without_overrap[e] == pid[f]]
    # 같은 pid경로를 리스트로 저장
    pidpath.sort() # 한 pid에 대한 경로의 리스트를 오름차순으로 정리
    j=1 # 주기용 j
    print('PID:%s 파일수:%s' %(
        pid_without_overrap[e],len(pidpath)), end=' ')
    # pid_list_in_csv_txtfile = [] # pid_without_overrap에 포함되는 pidpath안에 pid를 더해 text 파일화
    
    
    for h in tqdm(range(0,len(pidpath)),desc=('PID:%s' %pid_without_overrap[e])):
        df = pd.read_csv(pidpath[h], names = ['1', '2', '3'])
        # 내용 확인을 위해 csv를 df로 불러와서 
        # pid_list_in_csv_txtfile.append(os.path.basename(str(pidpath[h]))[:-4] + '\n')
        if df['1'].sum() == 0 or df['2'].sum() == 0 or df['3'].sum() == 0:         
            # 칼럼 1,2,3,을 각자 다 더해서 0이면 데이터가 없는 것이므로            
            continue # csv를 만들지 않고 넘어가기
        df.to_csv('%s/%s/%s(%s).csv' %(output_path,pid_without_overrap[e],
                    pid_without_overrap[e],j), index = False, header = None)
        # 데이터 있는 경우만 다시 csv로 만들기
        j+=1 # 주기용 +1
    print('살아남은 csv파일 갯수 %s' %(j-1))
    
    if len(os.listdir('%s%s' %(output_path,pid_without_overrap[e]))) == 0:
        f = open('%s%s/쓸수없는 PID' %(output_path,pid_without_overrap[e]), 'w')
        f.close()
        # with open('%s/%s/%s.txt' %(output_path,pid_without_overrap[e],
    #     pid_without_overrap[e]), 'w') as f: # paht2/pid 경로에 pid명으로 txt생성
    #     f.writelines(pid_list_in_csv_txtfile) # 생성한 pid.txt에 이어붙인 파일 목록을 넣어라
    
    
    
        
        
        
        