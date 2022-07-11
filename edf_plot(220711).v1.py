# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 16:06:23 2022

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
import pyedflib
import matplotlib.pyplot as plt
# edf 플랏 확인

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
filename = file_path_list[0]

f = pyedflib.EdfReader(filename) # pydeflib클래스에서 EdfReader 변수를 f에 선언
n = f.signals_in_file # 파일 내에 signal 정보를 n에 저장
signal_labels = f.getSignalLabels() # signal_labels불러오기
sigbufs = np.zeros((n, f.getNSamples()[0])) 
# sigbufs에 샘플 갯수 맞춰서 배열 생성 리스트랑 다르게 미리 크기를 만들 수 밖에 없음
for i in np.arange(n): # 만들어진 배열에 값을 넣어주자
    sigbufs[i, :] = f.readSignal(i)
    
plt.plot(sigbufs)
