# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 10:33:50 2022

@author: chang
"""
import numpy as np
from pyedflib import highlevel
import matplotlib.pyplot as plt
import os
import pandas as pd
import random
import shutil


file = "'C:/Users/chang/Desktop/rader_PID/chb02_01.edf"

def search_annotations_edf(dirname): # annotations파일 이름이 Hyponogram.edf이기 때문에 해당 파일을 찾기 위한 함수
    filenames = os.listdir(dirname)
    filenames = [file for file in filenames if file.endswith("chb02_01.edf")]
    return filenames

def search_signals_edf(dirname): # signals 파일 이름이 PSG.edf이기 때문에 해당 파일을 찾기 위한 함수
    filenames = os.listdir(dirname)
    filenames = [file for file in filenames if file.endswith("PSG.edf")]
    return filenames

def search_correct_annotations(dirname,filename): # signals파일에 대한 annotations을 저장하고 있는 파일을 찾기 위한 함수
    search_filename = filename.split('-')[0][:-2]
    file_list = os.listdir(dirname)
    filename = [file for file in file_list if search_filename in file if file.endswith("Hypnogram.edf")]

    return filename
 # npy형태로 변환 후 사용할 메소드들
def search_signals_npy(dirname):
    filenames = os.listdir(dirname)
    filenames = [file for file in filenames if file.endswith(".npy")]
    return filenames

def search_correct_annotations_npy(dirname,filename):
    search_filename = filename.split('-')[0][:-2]
    file_list = os.listdir(dirname)
    filename = [file for file in file_list if search_filename in file if file.endswith("npy")]

    return filename

def search_correct_signals_npy(dirname,filename):
    search_filename = filename.split('-')[0][:-2]
    file_list = os.listdir(dirname)
    filename = [file for file in file_list if search_filename in file if file.endswith("npy")]

    return filename

path = 'D:/dataset/data_2013/' # sleep-edf 2013 데이터를 가지고 있는 폴더 명
annotations_edf_list = search_annotations_edf(path)
signals_edf_list = search_signals_edf(path)

print('signals edf file list')
print(signals_edf_list)

print('annotations edf file list')
print(annotations_edf_list)

for filename in signals_edf_list:
    print('signals file name : %s , annotations file name : %s'%(filename,search_correct_annotations(path,filename)[0]))
    
epoch_size = 30
sample_rate = 100
save_signals_path = path + 'origin_npy/'
save_annotations_path = save_signals_path+'annotations/'

os.makedirs(save_annotations_path,exist_ok=True)
os.makedirs(save_signals_path,exist_ok=True)

for filename in signals_edf_list:
    signals_filename = filename
    annotations_filename = search_correct_annotations(signal_path,filename)[0]

    signals_filename = path + signals_filename
    annotations_filename = path + annotations_filename

    _, _, annotations_header = highlevel.read_edf(annotations_filename)

    label = []
    for ann in annotations_header['annotations']:
        start = ann[0]

        length = ann[1]
        length = int(str(length)[2:-1]) // epoch_size 
        # label은 30초 간격으로 사용할 것이기 때문에 30으로 나눈 값이 해당 sleep stage가 반복된 횟수이다.

        if ann[2] == 'Sleep stage W':
            for time in range(length):
                label.append(0)
        elif ann[2] == 'Sleep stage 1':
            for time in range(length):
                label.append(1)
        elif ann[2] == 'Sleep stage 2':
            for time in range(length):
                label.append(2)
        elif ann[2] == 'Sleep stage 3':
            for time in range(length):
                label.append(3)
        elif ann[2] == 'Sleep stage 4':
            for time in range(length):
                label.append(3)
        elif ann[2] == 'Sleep stage R':
            for time in range(length):
                label.append(4)
        else:
            for time in range(length):
                label.append(5)
    label = np.array(label)
    signals, _, signals_header = highlevel.read_edf(signals_filename)


    signals_len = len(signals[0]) // sample_rate // epoch_size
    annotations_len = len(label)
    if signals_header['startdate'] == annotations_header['startdate']:
        print("%s file's signal & annotations start time is same"%signals_filename.split('/')[-1])

        if signals_len > annotations_len :
            signals = signals[:3][:annotations_len]
        elif signals_len < annotations_len :
            signals = signals[:3]
            label = label[:signals_len]
        else:
            signals = signals[:3]
        signals = np.array(signals)

        np.save(save_signals_path + signals_filename.split('/')[-1].split('.')[0],signals)
        np.save(save_annotations_path + annotations_filename.split('/')[-1].split('.')[0],label)

        if (len(signals[0])//sample_rate//epoch_size != len(label)):
            print('signals len : %d / annotations len : %d'%(len(signals[0])//sample_rate//epoch_size,len(label)))

    else:
        print("%s file''s signal & annotations start time is different"%signals_filename.split('/')[-1])
        
epoch_size = 30
sample_rate = 100

path =  'D:/dataset/data_2013/origin_npy/'

signals_npy_list = search_signals_npy(path)

print(signals_npy_list)

channel_name_list = ['Fpz-Cz/','Pz-Oz/','EOG/']
for channel_index,channel_name in enumerate(channel_name_list):
    save_path = path + channel_name
    os.makedirs(save_path,exist_ok=True)

    for filename in signals_npy_list:
        signals_filename = filename

        signals_filename = path + signals_filename

        signals = np.load(signals_filename)

        signals = signals[channel_index].reshape(1,-1)
        print(signals.shape)

        np.save(save_path + filename,signals)
        
epoch_size = 30
sample_rate = 100

path =  'D:/dataset/data_2013/origin_npy/Fpz-Cz/'
annotations_path = 'D:/dataset/data_2013/origin_npy/annotations/'
signals_npy_list = search_signals_npy(path)

print(signals_npy_list)


for filename in signals_npy_list:
    signals_filename = path + filename
    annotations_filename = annotations_path+search_correct_annotations_npy(annotations_path,filename)[0]
    signals = np.load(signals_filename)
    label = np.load(annotations_filename)
    if len(signals[0])//sample_rate//epoch_size != len(label):
        print('%s is fault'%filename)
        
        