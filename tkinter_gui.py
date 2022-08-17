# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 17:20:53 2022

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
from tkinter import *
#  예제 1) tkinter 파이썬 GUI 레이블(label)
# tkinter를 사용하여 텍스트를 나타내보자

# 1. 루트화면 (root window) 생성
root = Tk() 
# 2. 텍스트 표시
# label = Label(tk,text='Hello World!') 
# 3. 레이블 배치 실행
# label.pack()
# 4. 메인루프 실행
root.mainloop()
