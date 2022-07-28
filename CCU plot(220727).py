# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 10:17:20 2022

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

input_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/CCU_databa10(concat)/CCU_databa(0) - txt-omission'

file_path_list = []
file_name_list = []

for (root, directories, files) in tqdm(os.walk(input_path)):
    # 경로를 3가지로 분리해서 가져옴/root:폴더 경로/files:파일명
    for file in (files): # files에서
        if file.endswith('.csv'): # .csv 확장자 인거만 가져와서
            file_name = file[:-4]
            file_path = os.path.join(root, file)
            # 경로와 파일명 합쳐서 file_path에 합쳐주고 누적은 안되니
            file_name_list.append(file_name)
            file_path_list.append(file_path)
            # 만들때 마다 리스트에 저장하자

# for h in range(0,file_path):
df = pd.read_csv(file_path_list[0], names = ['1', '2', '3'])

plt.plot(df)
plt.show()

plt.plot(df['2'])
plt.show()
