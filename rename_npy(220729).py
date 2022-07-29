# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 10:36:18 2022

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
from os.path import getsize
#%%
input_path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/edf_npy(1)/'

g=0
for (root, directories, files) in os.walk(input_path):
    print(g, end=' ')
    # 경로를 3가지로 분리해서 가져옴/root:폴더 경로/files:파일명
    g+=1
    if files[0].endswith('.csv'):
        continue
    # if root == '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/edf_npy(1)/chb23_08':
    #     print(root[76:],files[0],files[1])
    #     break
    if getsize('%s/%s' %(root,files[1])) <= getsize('%s/%s' %(root,files[0])):        
        if files[0][:8] != files[1][8:]:
            os.rename('%s/%s' %(root,files[0]),'%s/%s.npy' %(root,root[76:]))
            os.rename('%s/%s' %(root,files[1]),'%s/%s_label.npy' %(root,root[76:]))
    else:
        if files[1][:8] != files[0][:8]:
            os.rename('%s/%s' %(root,files[1]),'%s/%s.npy' %(root,root[76:]))
            os.rename('%s/%s' %(root,files[0]),'%s/%s_label.npy' %(root,root[76:]))
    
    