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

def importdf(name:str, delimit:str):  
    df = pd.read_csv(name,sep=delimit,header=None, names=["pt","eta","phi","charge"])
    return df
