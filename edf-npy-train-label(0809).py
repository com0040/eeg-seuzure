# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 10:00:34 2022

@author: chang
"""
#%% 패키지 불러오기
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
from os.path import getsize
#%% 불러올 파일 경로 / 확장자들(edf/txt/seizures) 별로 리스트화 
file_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit-scalp-eeg-database-1.0.0/chb-mit-scalp-eeg-database-1.0.0/'
output_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/edf_npy(2)/'
# file_name = pyedflib.data.get_generator_filename()
file_path_list = []
file_label = []
file_seizure = []
print('경로에서 .edf만 가져와서 file_path_lsit에 저장', end = ' ')

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
#%% 데이터 생성 폴더 곂치지 않게 만들기
filename='edf_npy' #파일명 고정값     
uniq=1 # 파일명에 추가할 숫자
while os.path.exists(output_path):  #동일한 파일명이 존재할 때=true 아닐때 false
  output_path='//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/%s(%d)' % (
      filename,uniq) #파일명(1) 파일명(2)...
  uniq+=1 # 반복되면서 숫자 증가
os.mkdir('%s' %(output_path)) 
print('폴더명 = %s' %(output_path[65:75]))
# 파일명도 저장되어 있는 output_path로 폴더생성/이후에 저장될 경로이기도 함
#%% 라벨txt->csv / 한눈에 보기 좋다
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
#%% 만든 csv 발작 여부 확인->시간라벨  
df = pd.read_csv('//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/all_chb.csv',
                 on_bad_lines='skip')
# 생성한 csv파일을 df로 불러온다
df = df.fillna(0) # nan으로 표시된 것을 0으로 바꿔준다
# PaserError : --> on_bad_lines='skip'(해결)
g=0 # 반복 카운트 용
for k in file_path_list: # 파일 경로에서 라벨과 데이터 빼올 것이다
    # if os.path.exists('%s%s' %(output_path,k[125:133])):
    #     print('이미 생성됨! 총 %s개 %d번 끝' %(len(file_path_list),g+1),k[125:133])
    #     g+=1 # 이미 생성된 시저파일 건너뛰기
    #     continue # 이미 있으면 다음 k로 / g+=1은 생략되지않게    
    file_edf = pyedflib.EdfReader(k) # pydeflib클래스에서 EdfReader 변수를 f에 선언
    n = file_edf.signals_in_file # 파일 내에 signal 정보를 n에 저장
    if n != 23: # 채널 수가 이상하면 
        print('총 %s개 %d번 시작' %(len(file_path_list),g+1),'채널오류', 'n = %s' %n, k[125:133])
        g+=1 # 카운팅 +1
        continue # 진행불가
    signal_labels = file_edf.getSignalLabels() # signal_labels불러오기
    sigbufs = np.zeros((n, file_edf.getNSamples()[0]))
    # sigbufs에 샘플 갯수 맞춰서 배열 생성 리스트랑 다르게 미리 크기를 만들 수 밖에 없음
    sigbufs_label = np.zeros((1,file_edf.getNSamples()[0]))
    # sigbufs와 다르게 채널에 0 or 1 이 들어가는 생성
    print('총 %s개 %d번 시작' %(len(file_path_list),g+1), end=' ') # 진행도 확인
    print(sigbufs_label.shape, '생성 중',k[125:133], end = ' ') # 오류났을 때 파일명 확인
    g+=1 # 카운팅용
    no_seizure = 1 # 시저 카운팅용
       
    for t in file_seizure: # seizure로 끝나는 파일 불러오고
        if k[125:] == 'chb13_40.edf': # 오류나는 파일
            print('chb13_40.edf 오류파일')
            break # 건너뛰기
        if t[125:137] == k[125:]: # 파일명이 일치하는지 확인한다
            print('찾았다', end = ' ') # 일치하면
            list_df = list(np.array(df[df['File Name'] == '%s\n' %t[125:137]]))
            # 전체 파일명과 시간있는 csv파일에서 파일명 열을 불러오면 발작시간을 불러올수 있음
            # 즉 csv파일을 리스트화 하는 작업/계속 0 열에 새로운 데이터를 넣어주므로 초기화x
            # index=0(파일명),1(시저유무),2(발작1시작),3(발작1끝)
            # 4(발작2시작), 5(발작2끝), 6(발작3시작), 7(발작3끝)
            sigbufs_label[0][int(list_df[0][2]*256):int(list_df[0][3]*256)] = 1
            # 파일의 라벨에 1을 넣어주는 조건
            # 첫 발작시간*256Hz(sample rate)=시작데이터~첫 발작 끝시간*256Hz=끝데이터
            if list_df[0][4] != 0 : # 발작 2일 경우
                sigbufs_label[0][int(list_df[0][4]*256):int(list_df[0][5]*256)] = 1
            if list_df[0][6] != 0 : # 발작 3일 경우
                sigbufs_label[0][int(list_df[0][6]*256):int(list_df[0][7]*256)] = 1
            break # 발작시간 넣는 목적 끝났으니 종료
        elif t==(file_seizure[-1]): # 마지막 파일이라면
            print('no seizure signal ',end = ' ')
            no_seizure = 0 # k : 전체 경로 중 하나 
    if no_seizure == 0: # 시저 시그널이 없다면
        print('진행 종료')
        continue # 아래코드 무시 
        
    # 혹시 곂치는 경우 새로 덮어쓰기
    if os.path.exists('%s/%s/%s_label.npy' % (output_path, k[125:133], k[125:133])):
         print('파일 삭제',end = ' ')
         os.remove('%s/%s/%s_label.npy' % (output_path, k[125:133], k[125:133]))
         # np.save('%s%s/%s_label' % (output_path, k[125:133], k[125:133]), sigbufs_label) 
         # print('배열모양', sigbufs.shape, '.npy 생성 중', end=' ')
    if os.path.exists('%s/%s/%s.npy' % (output_path, k[125:133], k[125:133])):
         print('파일 삭제',end = ' ')
         os.remove('%s/%s/%s.npy' % (output_path, k[125:133], k[125:133]))
    for j in np.arange(23): # 만들어진 배열에 값을 넣어주자
        sigbufs[j,:] = file_edf.readSignal(j) # 시그널을 읽어서 하나하나 넣어줌 
        
    # 데이터 리셰입
    # 라벨과 데이터 (-1,x,4096)으로 자르기
    # reshape로 형태 바꾸면 라벨 이상함?
    sigbufs = sigbufs[:,0:(len(sigbufs[0])//4096)*4096]
    # 배열을 4096크기로 나누어 떨어지지 않을 지 모르니
    sigbufs_label = sigbufs_label[:,0:(len(sigbufs_label[0])//4096)*4096] # 라벨도 마찬가지
    
    num_of_arr = sigbufs.reshape(-1,23,4096) # 23*4096으로 몇개의 데이터나오는지 계산
    sigbufs_label_arr = np.zeros((len(num_of_arr),1,4096)) # 빈 라벨 배열 만들기(크기맞춰)
    sigbufs_arr = np.zeros((len(num_of_arr),23,4096)) # 빈 배열 만들기(크기맞춰)  
    
    for a in range(len(num_of_arr)): # 데이터 길이만큼 4096만큼 자를거임         
        label_change = sigbufs_label[0,a*4096:a*4096+4096]
        sigbufs_label_arr[a,0,0:4096] = label_change
        # 라벨은 채널이 한개라서 포문 한개로 가능
        for b in range(22): # a 한개당 23개 채널 다 넣어주기 
            sigbufs_arr[a,b,0:4096] = sigbufs[b,a*4096:a*4096+4096]
   # 데이터 중 1들어간 부분만 뽑으려 했으나 한 파일에 들어있는 것을 뺄 필요는 없었음 --> 1 포함이어야함        
    
    # 유넷은 세그먼트 가능해야하므로 0만있는 데이터 필없음
    num_seizure_in_4096 = 0 # [0,4096] 평면에 일때 ?에 들어갈 숫자
    index_list = [] # 발작 있을때 평면의 인덱스 저장할 리스트
    for i in range(len(sigbufs_label_arr[:,0,0])): # 고정된 값 제외한 인덱스의 길이만큼 반복
        if np.any(sigbufs_label_arr[i,0,:])==1: # seizure가 있는지 확인
            index_list.append(i) # 있는 인덱스 넘버를 리스트로 저장해서
            num_seizure_in_4096 += 1 # 나중에 있는 것만 모을생각
            # 배열 생성할때 사용할 크기를 알아야해서 num_seizure_in_4096 지정
    
    sigbuf_label_with_seizure = np.where(sigbufs_label_arr==1)
    # 라벨 중 1을 모두 뽑으면 점의 인덱스가 나옴
    # [0] 변하는 값 데이터랑 라벨이랑 크기는 같음 [1] 1이 라벨된 고정 인덱스 [2] 고정 4096의 인덱스
    
    if (sigbuf_label_with_seizure[0].size == 0):
        # 시저없으면 만들 이유없으니 seizure가 없는 데이터 날리기 2차
        print('시저 없으니까 돌아가자') # 
        continue # 아래 코드는 무시
    
    non_overrap_index=list(set(sigbuf_label_with_seizure[0]))
    # 곂치지않는 [0]의 인덱스를 데이터에 넣어서 1있는 평면만 가져오게
    sigbufs_last = np.zeros((num_seizure_in_4096,23,4096))
    sigbufs_last_label = np.zeros((num_seizure_in_4096,1,4096))
    # 1을 가진 인덱스 크기만큼 sigbufs 값을 담기위해 만듬
    
    # npy로 만드는 부분
    f = 0
    for i in non_overrap_index: # 인덱스만큼 반복
        sigbufs_last[f,:,:] = sigbufs_arr[i,:,:]
        sigbufs_last_label[f,:,:] = sigbufs_label_arr[i,:,:]
        f+=1
        # 만들어진 배열에 한 배열씩 불러와 넣어주기
        
    if os.path.exists('%s/%s' % (output_path, k[125:133])) == False:
        os.mkdir('%s/%s' %(output_path,k[125:133])) # path2에 pid명으로 폴더 생성
    print('최종 구조 ', sigbufs_label_arr.shape) # sigbufs.shape,
    np.save('%s/%s/%s' % (output_path, k[125:133], k[125:133]), sigbufs_last) # .npy 파일로 저장
    np.save('%s/%s/%s_label' % (output_path, k[125:133], k[125:133]), sigbufs_last_label)
    # .npy 파일로 저장    
    file_edf.close() # 열린 파일 닫기-메모리 누수 방지
    del  sigbufs_label, signal_labels, n, file_edf
    # del sigbufs,
    # 변수 누적 방지
# list_0 = [] # 
# for i in range(0,len(sigbuf_label_with_seizure[2])):
#     list_0.append(sigbuf_label_with_seizure[2][i])
#%% 병합 부분(라벨/학습)
label_list = []
train_list = []
file_path_list = []
for (root, directories, files) in os.walk(output_path):
    # 경로를 3가지로 분리해서 가져옴/root:폴더 경로/files:파일명
    for file in files: # files에서
        if file.endswith('.npy'): # .npy 확장자 인거만 가져와서
            file_path = os.path.join(root, file)
            # 경로와 파일명 합쳐서 file_path에 합쳐주고 누적은 안되니
            file_path_list.append(file_path)
            # 만들때 마다 리스트에 저장하자
            if 'label' in file: # 파일명에 'label'이 있으면
                label_list.append(file_path) # label_list에 경로 저장
            else: # 없으면
                train_list.append(file_path) # train_list에 경로 저장
                
for f in tqdm(train_list, desc='train.npy 합치는 중'): # npy 합치기
    add_npy = np.load('%s' %f).astype('int8') # 적은 용량으로 불러오기
    if f == train_list[0]: # 처음엔
        all_npy = add_npy # 그대로 all에 넣어줌
    else: # 처음만 아니면 됨
        all_npy = np.concatenate((all_npy, add_npy),axis=0).astype('int8')
        # 계속 더하자 느려도 배열크기 안맞춰도됨
                
for g in tqdm(label_list, desc='label.npy 합치는 중'): # 라벨도 합치기
    add_label_npy = np.load('%s' %g).astype('int8') # 적은 용량으로 불러
    if g == label_list[0]: # 처음에는
        all_label_npy = add_label_npy # 그대로 넣어 줌
    else: # 나머지는
        all_label_npy = np.concatenate((all_label_npy, add_label_npy),axis=0).astype('int8')
        # 적은 용량으로 라벨 만들기
        
# all_npy = all_npy.swapaxes(0,1) # 넣어줄 형태로 바꿔줌 (-1,23,4096)
# all_label_npy = all_label_npy.swapaxes(0,1) # (4096,23,-1)

np.save('%s/train' % (output_path), all_npy) # npy 파일로 만들자
np.save('%s/label' % (output_path), all_label_npy) # 라벨도 만들기
#%% 데이터 확인용 플랏
plt.plot((sigbufs_label[:,]))

plt.plot((sigbufs_label[:,:,1]))
plt.plot((sigbufs_label_arr[188,0,:]))

n = sigbufs_label
n3 = sigbufs_label

x = range(921600)
plt.xlim(766000,778000)
plt.plot(x,n[0])
