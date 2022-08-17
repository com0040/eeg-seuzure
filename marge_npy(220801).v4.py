# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 15:40:08 2022

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
from os.path import getsize

input_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/edf_npy(1)/'
output_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/edf_npy(1)/'

label_list = []
train_list = []
file_path_list = []
for (root, directories, files) in os.walk(input_path):
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
                continue
                train_list.append(file_path) # train_list에 경로 저장

# for f in tqdm(train_list, desc='train.npy 합치는 중'): # npy 합치기
#     add_npy = np.load('%s' %f).astype('int8') # 적은 용량으로 불러오기
#     if f == train_list[0]: # 처음엔 
    
#         all_npy = add_npy # 그대로 all에 넣어줌
#     else: # 처음만 아니면 됨
#         all_npy = np.concatenate((add_npy, all_npy),axis=2).astype('int8')
#         # 계속 더하자 느려도 배열크기 안맞춰도됨
for g in tqdm(label_list, desc='label.npy 합치는 중'): # 라벨도 합치기
    add_label_npy = np.load('%s' %g).astype('int8') # 적은 용량으로 불러
    if g == label_list[0]: # 처음에는
        all_label_npy = add_label_npy # 그대로 넣어 줌
    else: # 나머지는
        all_label_npy = np.concatenate((add_label_npy, all_label_npy),axis=2).astype('int8')
        # 적은 용량으로 라벨 만들기
 
# all_npy = all_npy.swapaxes(0,1) # 넣어줄 형태로 바꿔줌 (-1,23,4096)
all_label_npy = all_label_npy.swapaxes(0,1) # (4096,23,-1)

# np.save('%s/train' % (output_path), all_npy) # npy 파일로 만들자
np.save('%s/label' % (output_path), all_label_npy) # 라벨도 만들기