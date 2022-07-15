# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 16:19:09 2022

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

file_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit-scalp-eeg-database-1.0.0/chb-mit-scalp-eeg-database-1.0.0/'
# file_name = pyedflib.data.get_generator_filename()

file_path_list = []
for (root, directories, files) in tqdm(os.walk(file_path),
    desc='경로에서 .edf만 가져와서 file_path_lsit에 저장'):
    for file in files:
        if '.edf' in file:
            file_path = os.path.join(root, file)
            file_path_list.append(file_path)

list_sigbufs =[]
for k in tqdm(file_path_list, desc='edf -> sigbuf -> np -> lsit에 저장'):
    f = pyedflib.EdfReader(k)
    n = f.signals_in_file
    signal_labels = f.getSignalLabels()
    sigbufs = np.zeros((n, f.getNSamples()[0]))
    for i in np.arange(n):
            sigbufs[i, :] = f.readSignal(i)
    list_sigbufs.append(sigbufs)        
f.close()
