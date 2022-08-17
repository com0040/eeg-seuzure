# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 12:43:25 2022

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

path = '//192.168.45.194/MainLAB/LabMeeting/leechangjae/data/CCU_databa10(concat)/CCU_databa(1)/14348028/14348028(1).csv'
df = pd.read_csv(path,names = ['1', '2', '3']) 

plt.plot(df)
plt.show()