import math
import csv
import time
import torch
import os
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

if torch.cuda.is_available():
  tensor = tensor.to('cuda')

def calculate_single_data(startidx, endidx, phase=1.5, bincount=30):
    rlist = []
    for i in range(startidx, endidx+1):
        rlist.append(single_event_difference(i,phase))
    result = torch.cat(rlist,dim=0)
    x_df = pd.DataFrame(result, columns=['phi','eta'])
    sx, sy, sz = surfacedatapro(x_df, bincount, bincount, torch.pi+phase, -torch.pi+phase, 5.5)
    sz = sz.T/(endidx-startidx)
    return sx, sy, sz

def single_event_difference(i,phase=1.5):
    event = importpbdatanumpy(i).T
    phi = torch.tensor(event[2])
    eta = torch.tensor(event[1])
    deta = eta - eta.unsqueeze(-1)
    dphi = phi - phi.unsqueeze(-1)
    ids = torch.arange(0,len(phi))
    mask = torch.ones_like(dphi).scatter_(1,ids.unsqueeze(1),0.)
    dphi = dphi[mask.bool()]
    deta = deta[mask.bool()]
    pimask = (dphi > (torch.pi+phase))*(-1) + (dphi < (-torch.pi+phase))*1
    dphi += (pimask*2*torch.pi)
    result = torch.stack([dphi,deta],dim=1)
    return result

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

def importdphideta(event:int):
    if event <= -2 or event >= 22948:
        print("event number out of range")
        return
    filename = 'ProcessedDifferenceData/devent_' + str(event) + '.csv'
    # check if file exists
    if not os.path.isfile(filename):
        print("file not found")
        return
    dataset = pd.read_csv(filename,sep=',',header=None, names=["phi","eta"])
    return dataset

def importdphidetarange(start_index, end_index):
    if start_index < 0 or start_index > 22947 or end_index < 0 or end_index > 22947:
        print("event number out of range")
        return
    if start_index > end_index:
        print("start_index > end_index")
        return
    for i in range(start_index, end_index+1):
        filename = 'ProcessedDifferenceData/devent_' + str(i) + '.csv'
        # check if file exists
        if not os.path.isfile(filename):
            print("one of the file is not found, index number: ",i)
            return
    t0 = time.time()
    dataset = importdphideta(start_index)
    for i in range(start_index+1, end_index+1):
        filename = 'ProcessedDifferenceData/devent_' + str(i) + '.csv'
        datasetnow = importdphideta(i)
        dataset = pd.concat([dataset, datasetnow], ignore_index=True)
        if i % 100 == 0:
            print("importing event ",i, " time: ", time.time()-t0)
    return dataset

def surfacedata(dfdata, binx=25, biny = 25, rangex=3.15, rangey=6):
    zdat,xdat,ydat = np.histogram2d(dfdata['phi'], dfdata['eta'], bins=[binx,biny], range=[[-rangex,rangex],[-rangey,rangey]])
    xdat = xdat[:-1] + (xdat[1]-xdat[0])/2
    ydat = ydat[:-1] + (ydat[1]-ydat[0])/2
    return xdat, ydat, zdat

def surfacedatapro(dfdata, binx=25, biny = 25, rangexhigh=(-2+2*math.pi), rangexlow=-2, rangey=6):
    zdat,xdat,ydat = np.histogram2d(dfdata['phi'], dfdata['eta'], bins=[binx,biny], range=[[rangexlow,rangexhigh],[-rangey,rangey]])
    xdat = xdat[:-1] + (xdat[1]-xdat[0])/2
    ydat = ydat[:-1] + (ydat[1]-ydat[0])/2
    return xdat, ydat, zdat

def plot_3d_surface(xdata, ydata, zdata, zlim, title, zlabel, filename):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data.
    X = xdata
    Y = ydata
    X, Y = np.meshgrid(X, Y)
    Z = zdata

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.rainbow, antialiased=True)

    # Customize the z axis.
    ax.set_zlim(0, zlim)
    ax.zaxis.set_major_locator(LinearLocator(5))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.03f}')
    ax.set_xlabel('dphi')
    ax.set_ylabel('deta')
    ax.set_zlabel(zlabel)
    plt.title(title)

    # Add a color bar which maps values to colors.
    plt.savefig('SavedFig/'+filename)
    plt.show()

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
#                   说明：importdphideta 和 importdphidetarange 可以用来导入dphi/deta数据
#                   如果想要import dphi/deta数据，可以使用importdphideta导入单个event，
#                   或者使用importdphidetarange导入多个event的dphi 和 deta 数据。
#                   然，预处理还没有做完。全部预处理大概需要占用电脑空间20个GB
#                   如果导入全部event，大概可以从20个小时加速到两个小时。（需要预处理）
#             
#                                                                                                                                    
##############################################################################################################################