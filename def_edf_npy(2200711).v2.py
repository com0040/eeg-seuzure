# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 14:06:47 2022

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


# file_name = pyedflib.data.get_generator_filename()
def load_file(file_path):
    file_path_list = []
    for (root, directories, files) in tqdm(os.walk(file_path),
        desc='경로에서 .edf만 가져와서 file_path_list에 저장'):
        # 경로를 3가지로 분리해서 가져옴/root:폴더 경로/files:파일명
        for file in files: # files에서 
            if file.endswith('.edf'): # .edf 확장자 인거만 가져와서
                file_path = os.path.join(root, file) 
                # 경로와 파일명 합쳐서 file_path에 합쳐주고 누적은 안되니
                file_path_list.append(file_path)
                # 만들때 마다 리스트에 저장하자
    return file_path_list

def load_edf(n,sigbufs,f,file_path_list,k):
    for i in np.arange(n): # 만들어진 배열에 값을 넣어주자
        sigbufs[i, :] = f.readSignal(i) # 시그널을 읽어서 하나하나 넣어줌
        # 채널별로 불러오는듯?        
    if k == file_path_list[0]:# 처음에 all_sigbufs가 비어있으므로
           global add_sigbufs 
           add_sigbufs = sigbufs       
        # concat을 할 수 없으므로 값을 그대로 넣어줌
    else:
        add_sigbufs = np.concatenate((add_sigbufs,sigbufs), axis=1)
        # (23,4096,+)형태의 all_sigbufs에 3번째 축에 reshape를 계속 더해줌
    
    return add_sigbufs
                
def edf_to_npy(file_path_list):
    for k in tqdm(file_path_list, desc='edf -> sigbuf -> np -> lsit에 저장'):
        # 변환 과정을 한눈에 알아보자   
        f = pyedflib.EdfReader(k) # pydeflib클래스에서 EdfReader 변수를 f에 선언
        n = f.signals_in_file # 파일 내에 signal 정보를 n에 저장
        signal_labels = f.getSignalLabels() # signal_labels불러오기
        sigbufs = np.zeros((n, f.getNSamples()[0])) 
        # sigbufs에 샘플 갯수 맞춰서 배열 생성 리스트랑 다르게 미리 크기를 만들 수 밖에 없음
        
        all_sigbufs = load_edf(n, sigbufs, f, file_path_list, k)
        f.close() # 열린 파일 닫기-메모리 누수 방지
        del sigbufs, signal_labels, n, f  # 변수 누적 방지
        
    if len(all_sigbufs[0])%4096 !=0: # 배열을 4096크기로 나누어 떨어지지 않을때
        all_sigbufs = all_sigbufs[:,0:(len(all_sigbufs[0])//4096)*4096]
        all_sigbufs = all_sigbufs.reshape(23,4096,-1) 
    else:
        all_sigbufs = all_sigbufs.reshape(23,4096,-1)
    np.save('%sedf_to_npy' % output_path, all_sigbufs)
    
file_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit-scalp-eeg-database-1.0.0/chb-mit-scalp-eeg-database-1.0.0/'
output_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/'

file_path_list = load_file(file_path)
edf_to_npy(file_path_list)   