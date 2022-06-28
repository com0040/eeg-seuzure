# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 15:56:18 2022

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
from pidlist import pidlist # pidlist 파일에서 함수 전부 가져오기 

start_time = dt.datetime.now()

# '//192.168.45.194/Data/CCU_databa10/'
pidlist( '//192.168.45.194/Data/CCU_databa10/','C:/Users/chang/Desktop/d/')

end_time = dt.datetime.now()
print('시작 시간',start_time)
print('끝난 시간',end_time)

time_different =  end_time - start_time
print('총 걸린 시간(초)', time_different)
