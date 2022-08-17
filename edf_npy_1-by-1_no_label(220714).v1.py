# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 11:35:46 2022

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

file_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit-scalp-eeg-database-1.0.0/chb-mit-scalp-eeg-database-1.0.0/'
output_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/'
# file_name = pyedflib.data.get_generator_filename()

file_path_list = []
file_label = []
file_seizure = []
print('경로에서 .edf만 가져와서 file_path_lsit에 저장')
for (root, directories, files) in os.walk(file_path):
    # 경로를 3가지로 분리해서 가져옴/root:폴더 경로/files:파일명
    for file in files: # files에서 
        if file.endswith('.edf'): # .edf 확장자 인거만 가져와서
            file_path = os.path.join(root, file)
            # 경로와 파일명 합쳐서 file_path에 합쳐주고 누적은 안되니
            file_path_list.append(file_path)
            # 만들때 마다 리스트에 저장하자
        # elif file.endswith('.txt'): # 라벨들어있는 txt
        #     file_path = os.path.join(root, file) # 경로를 따서
        #     file_label.append(file_path) # 따로 저장
        # elif file.endswith('.seizures'):
        #     file_path = os.path.join(root, file)
        #     file_seizure.append(file_path)
'''
file_txt = open("//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/all_chb.csv", 'w', newline='')
# 파일명/발작유무/발작시작/발작끝 정보를 csv파일로 파일명은 all_chb
wr = csv.writer(file_txt)  # 주소안
wr.writerow(['File Name','Number of Seizures in File','Seizures 1 Start Time','Seizures 1 End Time',
             'Seizures 2 Start Time', 'Seizures 2 End Time','Seizures 3 Start Time','Seizures 3 End Time'])
for j in file_label: # 라벨된 데이터 불러와서 csv로 만들기
    if j != file_label[0]:
        file = open(j, 'r')
        lines = file.readlines() # lines라는 리스트에 한줄씩 저장
        list_line =[]
        for q in lines:                        
            if 'File Name:' in q:                
                list_line.append(q[11:])                     
            
            if 'Number of Seizures in File: 0' in q:
                list_line.append(0)
                wr.writerow(list_line)
                list_line = []
            elif 'Number of Seizures in File:' in q and 'Number of Seizures in File: 0' not in q:
                list_line.append(1) 
                                         
            if 'Seizure 1 Start Time' in q: # 라벨
                list_line.append(re.sub(r'[^0-9]','',q))
            elif 'Seizure 2 Start Time' in q:
                list_line.append(re.sub(r'[^0-9]','',q))
            elif 'Seizure 3 Start Time' in q:
                list_line.append(re.sub(r'[^0-9]','',q))
            elif 'Seizure Start Time' in q:
                list_line.append(re.sub(r'[^0-9]','',q))        
            elif 'Seizure 1 End Time' in q:
                list_line.append(re.sub(r'[^0-9]','',q))
            elif 'Seizure 2 End Time' in q:
                list_line.append(re.sub(r'[^0-9]','',q))
            elif 'Seizure 3 End Time' in q:
                list_line.append(re.sub(r'[^0-9]','',q))                
            elif 'Seizure End Time' in q:
                list_line.append(re.sub(r'[^0-9]','',q))
                                
            # elif 'File Start Time' in q:
            #     list_line.insert(2,re.sub(r'[^0-9]','',q))
            # elif 'File End Time' in q:
            #     list_line.insert(3,re.sub(r'[^0-9]','',q))
                
            if  len(q) == 1:
                 wr.writerow(list_line)
                 list_line = []
                 
        wr.writerow(list_line)     
file_txt.close()

df = pd.read_csv('//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/all_chb.csv',
                 on_bad_lines='skip')
df = df.fillna(0)
# PaserError : on_bad_lines='skip'(해결)'''
g=0
for k in range(0,len(file_path_list)): # 변환 과정을 한눈에 알아보자
    if k >359:
        file_edf = pyedflib.EdfReader(file_path_list[k]) # pydeflib클래스에서 EdfReader 변수를 f에 선언
        n = file_edf.signals_in_file # 파일 내에 signal 정보를 n에 저장
        signal_labels = file_edf.getSignalLabels() # signal_labels불러오기
        sigbufs = np.zeros((23, file_edf.getNSamples()[0]))
        # sigbufs에 샘플 갯수 맞춰서 배열 생성 리스트랑 다르게 미리 크기를 만들 수 밖에 없음
        # sigbufs_label = np.zeros((1,file_edf.getNSamples()[0]))
        # sigbufs에 샘플 갯수 맞춰서 0으로 초기화된 배열 생성
        print('총 %s개 %d번' %(len(file_path_list),g+1), end=' ')
        print(sigbufs.shape, '생성 중', end=' ')
        # for t in file_seizure: # seizure 있는지 확인하고 sigbufs_label에 표기
        #     if t[125:137] == k[125:]: # seizure 있으면 
        #         print('찾앗다', end=' ')
        #         list_df = list(np.array(df[df['File Name'] == '%s\n' %t[125:137]]))          
        #         # index=0(파일명),1(시저유무),2(발작1시작),3(발작1끝)
        #         # 4(발작2시작), 5(발작2끝), 6(발작3시작), 7(발작3끝)                    
        #         sigbufs_label[:,int(list_df[0][2]*256):int(list_df[0][3]*256)] = 1   
        #         if list_df[0][4] != 0 :
        #             sigbufs_label[:,int(list_df[0][4]*256):int(list_df[0][5]*256)] = 1
        #         if list_df[0][6] != 0 :
        #             sigbufs_label[:,int(list_df[0][6]*256):int(list_df[0][7]*256)] = 1 
                   
        # np.save('%s%s_label' % (output_path, file_path_list[g][125:133]), sigbufs_label)
        # print('배열모양', sigbufs.shape, '.npy 생성 중', end=' ')
        for i in np.arange(22):
            print(i,end='')# 만들어진 배열에 값을 넣어주자
            sigbufs[i, :] = file_edf.readSignal(i) # 시그널을 읽어서 하나하나 넣어줌
            
            # 채널별로 불러오는듯?
        if len(sigbufs[0])%4096 !=0: # 배열을 4096크기로 나누어 떨어지지 않을때
            sigbufs = sigbufs[:,0:(len(sigbufs[0])//4096)*4096]
            # sigbufs_label = sigbufs_label[0,0:(len(sigbufs_label[0])//4096)*4096]
            # 4096으로 나눠서 나머지 없에고 갯수 맞춘 후
            sigbufs = sigbufs.reshape(23,4096,-1) 
            # sigbufs_label = sigbufs_label.reshape(1,4096,-1) 
            # 3차원 모양으로 바꿈
        else:
            # sigbufs_label = sigbufs_label.reshape(1,4096,-1) 
            sigbufs = sigbufs.reshape(23,4096,-1)
            # 나누어 떨어지면 그냥 바꿈
        print('최종 구조 ', sigbufs.shape) # sigbufs.shape,
        np.save('%s%s' % (output_path, file_path_list[g][125:133]), sigbufs) # .npy 파일로 저장 
        # np.save('%s%s_label' % (output_path, file_path_list[g][125:133]), sigbufs_label) # .npy 파일로 저장 
        
        file_edf.close() # 열린 파일 닫기-메모리 누수 방지
        del  sigbufs, signal_labels, n, file_edf
    g+=1  
        # del sigbufs,
        # 변수 누적 방지
