import math
import csv
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

def importdf(fileaddress:str, delimit:str):  
    df = pd.read_csv(fileaddress,sep=delimit,header=None, names=["pt","eta","phi","charge"])
    return df

def importpbdatapandas(event:int): # if event = -1 then import all events.
    if event <= -2 or event >= 22948:
        print("event number out of range")
        return
    if event != -1:
        filename = 'ProcessedData/pbpb_' + str(event) + '.csv'
        dataset = importdf(filename, ',')
    else:
        dataset = importdf("ProcessedData/pbpb_0.csv", ',')
        for i in range(1, 22948):
            filename = 'ProcessedData/pbpb_' + str(i) + '.csv'
            datasetnow = importdf(filename, ',')
            dataset = pd.concat([dataset, datasetnow])
            print("importing event ",i)
    return dataset

def importpbdatanumpy(event:int):
    if event <= -2 or event >= 22948:
        print("event number out of range")
        return
    if event != -1:
        filename = 'ProcessedData/pbpb_' + str(event) + '.csv'
        dataset = np.loadtxt(filename, delimiter=',')
    else:
        dataset = np.loadtxt("ProcessedData/pbpb_0.csv", delimiter=',')
        for i in range(1, 22948):
            filename = 'ProcessedData/pbpb_' + str(i) + '.csv'
            datasetnow = np.loadtxt(filename, delimiter=',')
            dataset = np.concatenate((dataset, datasetnow))
            print("importing event ",i)
    return dataset

def importpdrange(start_event_index, end_event_index):
    if start_event_index < 0 or start_event_index > 22947 or end_event_index < 0 or end_event_index > 22947:
        print("event number out of range")
        return
    if start_event_index > end_event_index:
        print("start_event_index > end_event_index")
        return
    dataset = importpbdatapandas(start_event_index)
    for i in range(start_event_index+1, end_event_index+1):
        filename = 'ProcessedData/pbpb_' + str(i) + '.csv'
        datasetnow = importdf(filename, ',')
        dataset = pd.concat([dataset, datasetnow], ignore_index=True)
        print("importing event ",i)
    return dataset

def importnprange(start_event_index, end_event_index):
    if start_event_index < 0 or start_event_index > 22947 or end_event_index < 0 or end_event_index > 22947:
        print("event number out of range")
        return
    if start_event_index > end_event_index:
        print("start_event_index > end_event_index")
        return
    dataset = importpbdatanumpy(start_event_index)
    for i in range(start_event_index+1, end_event_index+1):
        filename = 'ProcessedData/pbpb_' + str(i) + '.csv'
        datasetnow = datasetnow = np.loadtxt(filename, delimiter=',')
        dataset = np.concatenate((dataset, datasetnow))
        print("importing event ",i)
    return dataset
    

##############################################################################################################################
#                                                  Utility Functions                                                      
#                                                                              
#                   说明：如果想要import pbpb data，可以使用importpbdatapandas 或者importpbdatanumpy
#                   如果要import特定的event number的话输入0-22947之间的数字                                                
#                   如果要import所有event的话输入-1即可。
#
#                   e.g. >>> event_0 = importpbdatapandas(0) 我们使用pandas导入了序号为0的event
#                   e.g. >>> event_all =  importpbdatapandas(-1) 我们使用pandas导入了所有event (大概要等2-3min)                 
#                                                                                                                                    
##############################################################################################################################