# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 15:08:51 2022

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
import datetime as dt # from pidlist import pidlist # pidlist 파일에서 함수 전부 가져오기
from tqdm import tqdm
import pyedflib

# df 일때 메모리 줄이는 함수 
def reduce_mem_usage(sigbufs_list, verbose=True):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = sigbufs_list.memory_usage().sum() / 1024**2    
    for col in sigbufs_list.columns:
        col_type = sigbufs_list[col].dtypes
        if col_type in numerics:
            c_min = sigbufs_list[col].min()
            c_max = sigbufs_list[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    sigbufs_list[col] = sigbufs_list[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    sigbufs_list[col] = sigbufs_list[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    sigbufs_list[col] = sigbufs_list[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    sigbufs_list[col] = sigbufs_list[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    sigbufs_list[col] = sigbufs_list[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    sigbufs_list[col] = sigbufs_list[col].astype(np.float32)
                else:
                    sigbufs_list[col] = sigbufs_list[col].astype(np.float64)    
    end_mem = sigbufs_list.memory_usage().sum() / 1024**2
    if verbose: print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(end_mem, 100 * (start_mem - end_mem) / start_mem))
    return sigbufs_list

file_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit-scalp-eeg-database-1.0.0/chb-mit-scalp-eeg-database-1.0.0/'
output_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/'
# file_name = pyesigbufs_listlib.data.get_generator_filename()

file_path_list = []
for (root, directories, files) in tqdm(os.walk(file_path),
    desc='경로에서 .edf만 가져와서 file_path_lsit에 저장'):
    # 경로를 3가지로 분리해서 가져옴/root:폴더 경로/files:파일명
    for file in files: # files에서 
        if file.endswith('.edf'): # .edf 확장자 인거만 가져와서
            file_path = os.path.join(root, file) 
            # 경로와 파일명 합쳐서 file_path에 합쳐주고 누적은 안되니
            file_path_list.append(file_path)
            # 만들때 마다 리스트에 저장하자

sigbufs_list = []
for k in tqdm(file_path_list, desc='edf -> sigbuf -> np -> lsit에 저장'):
    # 변환 과정을 한눈에 알아보자   
    f = pyedflib.EdfReader(k) # pydeflib클래스에서 EdfReader 변수를 f에 선언
    n = f.signals_in_file # 파일 내에 signal 정보를 n에 저장
    signal_labels = f.getSignalLabels() # signal_labels불러오기
    sigbufs = np.zeros((n, f.getNSamples()[0])) 
    # sigbufs에 샘플 갯수 맞춰서 배열 생성 리스트랑 다르게 미리 크기를 만들 수 밖에 없음
    for i in np.arange(n): # 만들어진 배열에 값을 넣어주자
        sigbufs[i, :] = f.readSignal(i) # 시그널을 읽어서 하나하나 넣어줌
        # 채널별로 불러오는듯? 
    if k == file_path_list[0]: # 메모리 감소를 위해 df변환
        sig_df = pd.DataFrame(sigbufs)
        # 첫 사이클에서 sig_df에 저장
    else:
        add_df = pd.DataFrame(sigbufs) # 두번째 부터는 add_df에 저장해서
        sig_df = pd.concat([sig_df,add_df],axis=1)
        del add_df
        # 가로(열)방향으로 합치기
    # sigbufs_list.append(sigbufs)
    # 분리된 데이터 리스트에 담기
    f.close() # 열린 파일 닫기-메모리 누수 방지
    del sigbufs, signal_labels, n, f

all_sigbufs = sig_df.to_numpy()
if len(all_sigbufs[0])%4096 !=0: # 배열을 4096크기로 나누어 떨어지지 않을때
    all_sigbufs = all_sigbufs[:,0:(len(all_sigbufs[0])//4096)*4096]
    # (23,x)형태의 자료에서 x자리를 4096크기 단위로 자르고
    all_sigbufs = all_sigbufs.reshape(23,4096,-1) 
    # (23,4096,y)형태로 분리
else: # 나누어 떨어지면
    all_sigbufs = all_sigbufs.reshape(23,4096,-1)
    # 그대로 분리
    
np.save('%sedf_to_npy' % output_path, all_sigbufs)
# npy 파일로 저장



# 3차원 np
# m,n,r = sigbufs.shape
# out_arr = np.column_stack((np.repeat(np.arange(m),n),sigbufs.reshape(m*n,-1)))
# out_df = pd.DataFrame(out_arr)

# 메모리 줄이기 ㅠ 다음 버전은 df로 바꿔서 해보고 아님 기원님 ㄱㄱ
# reduce_sigbufs = reduce_mem_usage(out_df)
# Mem. usage decreased to 40.61 Mb (75.0% reduction)