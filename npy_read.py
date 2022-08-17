# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 16:33:25 2022

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
from sklearn.preprocessing import minmax_scale
#%%
a = np.load('//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/edf_npy(2)/chb01_04/chb01_04.npy')
a = np.transpose(a,[2,1,0])
a1 = a[:,:,90]/abs(a[:,:,90]).max()
a1 = a/abs(a).max()
# a1 = minmax_scale(a[:,:,90])
a1 = a1.reshape(a.shape[0],a.shape[1],1)

b = np.load('//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/edf_npy(3)/chb01_04/chb01_04_label.npy')
b1 = np.transpose(b,[2,1,0])
plt.plot((b1[:,:,0]))

c = np.load('//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/chb-mit_npy/edf_npy(3)/chb01_03/chb01_03_label.npy')
c1 = np.transpose(c,[2,1,0])
plt.plot((c1[:,:,]))

all_label = np.zeros((21922,1,4096))

all_sig = np.concatenate((b,c),axis=0).astype('int8')
all_sig_1 = np.transpose(all_sig,[2,1,0]) 
plt.plot((all_sig_1[:,:,90]))

plt.plot((a1[:,0,0]))
plt.plot((a[:,0,91]))
plt.plot((n[:,100]))

n = sigbufs_label
n3 = sigbufs_label

x = range(921600)
plt.xlim(0,921600)
plt.plot(x,n[0])