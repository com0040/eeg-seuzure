# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 17:48:14 2022

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

    
def file_path():
    file_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit-scalp-eeg-database-1.0.0/chb-mit-scalp-eeg-database-1.0.0/'
    output_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/'
    # file_name = pyedflib.data.get_generator_filename()
    file_path_list = []
    print('경로에서 .edf만 가져와서 file_path_lsit에 저장')
    for (root, directories, files) in tqdm(os.walk(file_path)): # root 폴더임
        for file in files:
            if file.endswith('.edf'):
                file_path = os.path.join(root, file)
                file_path_list.append(file_path)
   
    return file_path_list, output_path

def edf_read_sigbuf():
    file_path_list, output_path = file_path()
    for k in tqdm(file_path_list, desc='edf -> sigbuf -> np -> lsit에 저장'):
        f = pyedflib.EdfReader(k) # pydeflib클래스에서 EdfReader 변수를 f에 선언
        n = f.signals_in_file # 파일 내에 signal 정보를 n에 저장
        signal_labels = f.getSignalLabels() # signal_labels불러오기
        sigbufs = np.zeros((n, f.getNSamples()[0])) # sigbufs에 샘플 갯수로 배열 길이 맞춰줌
        for i in np.arange(n):
            sigbufs[i, :] = f.readSignal(i)
        if len(sigbufs[0])%4096 !=0:
             sigbufs_divide_1 = sigbufs[0:(len(sigbufs)/4096)*4096] 
             sigbufs= sigbufs_divide_1
        reshape_sigbufs = sigbufs.reshape(23,4096,-1)    
        if k == file_path_list[0]:# 처음
            all_sigbufs = reshape_sigbufs
            del reshape_sigbufs
        else:
            all_sigbufs = np.concatenate((all_sigbufs,reshape_sigbufs), axis=2)
            del reshape_sigbufs
        f.close()
        del sigbufs, signal_labels, n, f
        
    np.save('%sedf_to_npy' % output_path, all_sigbufs) # x_save.npy
    
edf_read_sigbuf()