# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 14:26:32 2022

@author: chang
"""
import math
import string
import glob
import re
import os # 파일을 복사하거나 디렉터리를 생성하고 특정 디렉터리 내의 파일 목록 구하기
import csv
import pandas as pd # 행과 열로 구성된 객체 생성, 안정적 데이터 처리
 # import matplotlib.pyplot as plt # 시각화 패키지
import numpy as np # 고성능 과학 계산용 패키지
from numpy import *
import natsort
import sys
from pandas import DataFrame
import datetime as dt # from pidlist import pidlist # pidlist 파일에서 함수 전부 가져오기
from tqdm import tqdm
import pyedflib
#%% 

file_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit-scalp-eeg-database-1.0.0/chb-mit-scalp-eeg-database-1.0.0/'
output_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/edf_npy(1)/'
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
        elif file.endswith('.txt'): # 라벨들어있는 txt
            file_path = os.path.join(root, file) # 경로를 따서
            file_label.append(file_path) # 따로 저장
        elif file.endswith('.seizures'):
            file_path = os.path.join(root, file)
            file_seizure.append(file_path)

# filename='edf_npy' #파일명 고정값     

# uniq=1 # 파일명에 추가할 숫자
# while os.path.exists(output_path):  #동일한 파일명이 존재할 때=true 아닐때 false
#   output_path='//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/%s(%d)' % (
#       filename,uniq) #파일명(1) 파일명(2)...
#   uniq+=1 # 반복되면서 숫자 증가

# os.mkdir('%s' %(output_path)) 
# 파일명도 저장되어 있는 output_path로 폴더생성/이후에 저장될 경로이기도 함

#%%

file_txt = open("%s/all_chb.csv" % output_path, 'w', newline='')
# 파일명/발작유무/발작시작/발작끝 정보를 csv파일로 파일명은 all_chb
wr = csv.writer(file_txt)# 주소안
wr.writerow(['File Name','Number of Seizures in File','Seizures 1 Start Time','Seizures 1 End Time',
             'Seizures 2 Start Time', 'Seizures 2 End Time','Seizures 3 Start Time','Seizures 3 End Time'])
for j in file_label: # 라벨된 데이터 불러와서 csv로 만들기
    if j != file_label[0]: # 라벨[0]에 이상한거 들어있음/제외
        file = open(j, 'r') # 
        lines = file.readlines() # lines라는 리스트에 한줄씩 저장
        list_line =[] # 저장할 리스트
        for q in lines: # 라인을 한줄씩 검사
            if 'File Name:' in q: # 그 줄에 파일명이 있으면
                list_line.append(q[11:]) # 파일 명에 해당하는 것을 list_line에 추가
            # 파일명이 나오면 추가 후 한줄내리기
            if 'Number of Seizures in File: 0' in q: # 
                list_line.append(0)
                wr.writerow(list_line)
                list_line = []
            # 시저없는 파일을 0으로 라벨
            elif 'Number of Seizures in File:' in q and 'Number of Seizures in File: 0' not in q:
                list_line.append(1)
            # 시저 있는 파일은 1로 라벨                                 
            if 'Seizure 1 Start Time' in q:
                list_line.append(re.sub(r'[^0-9]','',q))
                # 숫자만 불러오기/re.sub()->해당 문자열을 불러와서 다른 문자로 변환
                # re.sub('바뀔','바꿀',해당 문장) []안에 ^ = not, 따라서 [^0-9]는 숫자를 제외함
                # 문자열 앞에 r이 붙으면 해당 문자열이 구성된 그대로 문자열로 반환
                # 즉 문자를 다 불러서 없엔다 = 숫자만 남음
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
                 wr.writerow(list_line) # 작성하고 다음줄로 넘어가기
                 list_line = []
                 
        wr.writerow(list_line)
file_txt.close() # 생성한 파일 닫기
#%%

df = pd.read_csv('//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/all_chb.csv',
                 on_bad_lines='skip')
# 생성한 csv파일을 df로 불러온다
df = df.fillna(0) # nan으로 표시된 것을 0으로 바꿔준다
# PaserError : --> on_bad_lines='skip'(해결)
g=0 # 반복 카운트 용
for k in file_path_list: # 변환 과정을 한눈에 알아보자
    if os.path.exists('%s%s' %(output_path,k[125:133])):
        print('총 %s개 %d번 시작' %(len(file_path_list),g+1), end=' ')
        g+=1 # 이미 생성된 시저파일 건너뛰기
        continue # 이미 있으면 다음 k로 / g+=1은 생략되지않게
    
    file_edf = pyedflib.EdfReader(k) # pydeflib클래스에서 EdfReader 변수를 f에 선언
    n = file_edf.signals_in_file # 파일 내에 signal 정보를 n에 저장
    if n != 23:
        print('총 %s개 %d번 시작' %(len(file_path_list),g+1),'채널오류', k[125:133], end=' ')
        continue
    signal_labels = file_edf.getSignalLabels() # signal_labels불러오기
    sigbufs = np.zeros((n, file_edf.getNSamples()[0]))
    # sigbufs에 샘플 갯수 맞춰서 배열 생성 리스트랑 다르게 미리 크기를 만들 수 밖에 없음
    sigbufs_label = np.zeros((1,file_edf.getNSamples()[0]))
    # sigbufs와 다르게 채널에 0 or 1 이 들어가는 생성
    print('총 %s개 %d번 시작' %(len(file_path_list),g+1), end=' ')
    print(sigbufs_label.shape, '생성 중',k[125:133])
    g+=1 # 카운팅용
    no_seizure = 1
    
    for t in file_seizure: # seizure로 끝나는 파일 불러오고 
        if k[125:] == 'chb13_40.edf': # 오류나는 파일
            print('chb13_40.edf 오류파일')
            break # 건너뛰기
        if t[125:137] == k[125:]: # 파일명이 일치하는지 확인한다
            
            print('찾앗다', end=' ') # 일치하면
            list_df = list(np.array(df[df['File Name'] == '%s\n' %t[125:137]]))
            # 전체 파일명과 시간있는 csv파일에서 파일명 열을 불러오면 발작시간을 불러올수 있음
            # 즉 csv파일을 리스트화 하는 작업/계속 0 열에 새로운 데이터를 넣어주므로 초기화x
            # index=0(파일명),1(시저유무),2(발작1시작),3(발작1끝)
            # 4(발작2시작), 5(발작2끝), 6(발작3시작), 7(발작3끝)                    
            sigbufs_label[:,int(list_df[0][2]*256):int(list_df[0][3]*256)] = 1
            # 파일의 라벨에 1을 넣어주는 조건
            # 첫 발작시간*256Hz(sample rate)=시작데이터~첫 발작끝시간*256Hz=끝데이터
            if list_df[0][4] != 0 : # 발작 2일 경우
                sigbufs_label[:,int(list_df[0][4]*256):int(list_df[0][5]*256)] = 1
            if list_df[0][6] != 0 : # 발작 3일 경우
                sigbufs_label[:,int(list_df[0][6]*256):int(list_df[0][7]*256)] = 1
            break
        elif t==(file_seizure[-1]): # 마지막 파일이라면
            no_seizure = 0 # 
            
    if no_seizure == 0:
        no_seizure = 1
        continue
                  
    # np.save('%s%s_label' % (output_path, file_path_list[g][125:133]), sigbufs_label)
    # print('배열모양', sigbufs.shape, '.npy 생성 중', end=' ')
    for i in np.arange(23): # 만들어진 배열에 값을 넣어주자
        sigbufs[i, :] = file_edf.readSignal(i) # 시그널을 읽어서 하나하나 넣어줌 
            
        # 채널별로 불러오는듯?
    if len(sigbufs_label[0])%4096 !=0: # 배열을 4096크기로 나누어 떨어지지 않을때
        sigbufs = sigbufs[:,0:(len(sigbufs[0])//4096)*4096]
        sigbufs_label = sigbufs_label[0,0:(len(sigbufs_label[0])//4096)*4096]
        # 4096으로 나눠서 나머지 없에고 갯수 맞춘 후
        sigbufs = sigbufs.reshape(23,4096,-1) 
        sigbufs_label = sigbufs_label.reshape(1,4096,-1)
        # 3차원 모양으로 바꿈 -1은 크기를 모르니 알아서 채우라는 말
    else:
        sigbufs_label = sigbufs_label.reshape(1,4096,-1)
        sigbufs = sigbufs.reshape(23,4096,-1)
        # 나누어 떨어지면 그냥 바꿈
                        
    # 유넷은 세그먼트 가능해야하므로 0만있는 데이터 필없음
    num_seizure_in_4096 = 0 # [0,4096] 평면에 일때 ?에 들어갈 숫자
    index_list = [] # 발작 있을때 평면의 인덱스 저장할 리스트
    for i in range(len(sigbufs_label[0,0,:])): # 고정된 값 제외한 인덱스로
        if np.any(sigbufs_label[0,:,i])==1: # seizure가 있는지 확인
            index_list.append(i) # 있는 인덱스 넘버를 리스트로 저장해서
            num_seizure_in_4096 += 1 # 나중에 있는 것만 모을생각 
            # 배열 생성할때 사용할 크기를 알아야해서 num_seizure_in_4096 지정
    
    sigbuf_label_with_seizure = np.where(sigbufs_label==1) 
    # 라벨 중 1을 모두 뽑으면 점의 인덱스가 나옴
    # [0] 1이 라벨된 고정 인덱스 [1] 고정 4096의 인덱스 [2] 변하는 값 데이터랑 라벨이랑 크기는 같음
    
    if (sigbuf_label_with_seizure[0].size == 0 and sigbuf_label_with_seizure[1].size == 0 
        and sigbuf_label_with_seizure[2].size == 0):
        # 시저없으면 만들 이유없으니 seizure가 없는 데이터 날리기 2차
        print('시저 없으니까 돌아가자')
        continue
    
    # non_overrap_index=list(set(sigbuf_label_with_seizure[2])) 
    # 곂치지않는 [2]의 인덱스를 데이터에 넣어서 1있는 평면만 가져오게

    sigbufs_last = np.zeros((23,4096,num_seizure_in_4096))
    # 1을 가진 인덱스 크기만큼 sigbufs 값을 담기위해 만듬

    for i in np.arange(len(index_list)): # 인덱스만큼 반복
          sigbufs_last[:,:,i] = sigbufs[:,:,index_list[i]] 
          # 만들어진 배열에 한 배열씩 불러와 넣어주기
    
    os.mkdir('%s/%s' %(output_path,k[125:133])) # path2에 pid명으로 폴더 생성
    print('최종 구조 ', sigbufs_last.shape) # sigbufs.shape,
    np.save('%s/%s/%s' % (output_path, k[125:133], k[125:133]), sigbufs_last) # .npy 파일로 저장
    np.save('%s/%s/%s_label' % (output_path, k[125:133], file_path_list[g][125:133]), sigbufs_label) 
    # .npy 파일로 저장
    
    file_edf.close() # 열린 파일 닫기-메모리 누수 방지
    del  sigbufs_label, signal_labels, n, file_edf
    # del sigbufs,
    # 변수 누적 방지
# list_0 = []
# for i in range(0,len(sigbuf_label_with_seizure[2])):
#     list_0.append(sigbuf_label_with_seizure[2][i])
    


