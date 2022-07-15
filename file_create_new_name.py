# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 17:29:47 2022

@author: chang
"""

import os
import csv
 
input_path = r'C:/Users/chang/Desktop/d/'
filename='sample_merge' #파일명 고정값
file_ext='.csv' #파일 형식
 
output_path='C:/Users/chang/Desktop/d/%s%s' %(filename,file_ext)
uniq=1
while os.path.exists(output_path):  #동일한 파일명이 존재할 때
  output_path='C:/Users/chang/Desktop/d/%s(%d)%s' % (filename,uniq,file_ext) #파일명(1) 파일명(2)...
  uniq+=1
