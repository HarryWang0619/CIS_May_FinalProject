import math
import csv
import time
import os
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

def surfacedata(dfdata, dx = 0.5, dy = 0.5, rangex=3.15, rangey=4):
    phi_c = math.ceil(rangex*2/dx)
    eta_c = math.ceil(rangey*2/dy)
    phi_data = np.arange(-rangex, rangex, dx)+dx/2
    eta_data = np.arange(-rangey, rangey, dy)+dy/2
    z_data = np.zeros([phi_c, eta_c], dtype=int)
    for index,instance in dfdata.iterrows():
        if instance['phi'] >= rangex or instance['phi'] <= -rangex or instance['eta'] >= rangey or instance['eta'] <= -rangey:
            continue
        phi_index = math.floor((instance['phi']+rangex)/dx) 
        eta_index = math.floor((instance['eta']+rangey)/dy)
        z_data[phi_index][eta_index] += 1
    return phi_data, eta_data, z_data.T

def plot_3d_surface(xdata, ydata, zdata, zlim, title, filename):
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
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')
    ax.set_xlabel('dphi')
    ax.set_ylabel('deta')
    ax.set_zlabel('S')
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