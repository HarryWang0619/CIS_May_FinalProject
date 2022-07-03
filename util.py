import math
import csv
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt


def importfilelist(name:str,delimit:str):
    # importfile('hw3_cancerdata.csv', '\t')
    file = open("datasets/"+name, encoding='utf-8-sig')
    reader = csv.reader(file, delimiter=delimit)
    dataset = []
    for row in reader:
        dataset.append(row)
    file.close()
    return dataset

def importdf(fileaddress:str, delimit:str):  
    df = pd.read_csv(fileaddress,sep=delimit,header=None, names=["pt","eta","phi","charge"])
    return df

def importpbdatapandas(event:int): # if event = -1 then import all events.
    if event <= -2 or event >= 29948:
        print("event number out of range")
        return
    if event != -1:
        filename = 'ProcessedData/pbpb_' + str(event) + '.csv'
        dataset = importdf(filename, ',')
        print(dataset)
    else:
        dataset = importdf("ProcessedData/pbpb_0.csv", ',')
        for i in range(1,2):
            filename = 'ProcessedData/pbpb_' + str(i) + '.csv'
            datasetnow = pd.read_csv(filename,sep=',',header=None)
            dataset = dataset.append(datasetnow)
            print("importing event ",i)
    return dataset
    
ds = importpbdatapandas(-1)
print(len(ds))
print(ds[0:100])