from utils import *
import time

def writehelper(i, writein):
    filename = 'ProcessedDifferenceData/devent_' + str(i) + '.csv'
    f = open(filename, 'w')
    writer = csv.writer(f)
    writer.writerows(writein)
    f.close()
    return

def d_data(event):
    deta=np.array([])
    dphi=np.array([])
    for i in range(len(event)-1):
        for j in range(i+1,len(event)-1):
            k = event['phi'][i]-event['phi'][j]
            if k < -math.pi:
                k += 2*math.pi
            elif k > math.pi:
                k -= 2*math.pi
            deta=np.append(deta,float("{:.3f}".format((event['eta'][i]-event['eta'][j]))))
            dphi=np.append(dphi,float("{:.3f}".format(k)))
    
    df = pd.DataFrame(np.vstack([dphi,deta]).T,columns=['phi','eta'])
    return df

def readandwrite_delta(): 
    # this function read file from ProcessedData/pbpb_*.csv
    # then calculate the difference between every two instances.
    # then write the difference to ProcessedDifferenceData/devent_*.csv
    writeidx = range(11600,12000) #22948
    print("start reading")
    t0 = time.time()
    all_events = [importpbdatapandas(i) for i in range(0, 22948)]
    for i in writeidx:
        print("start writing event", i)
        event = all_events[i]
        df = d_data(event)
        writehelper(i, df.values.tolist())
        if i % 5 == 0:
            print("time at event", i, ":", float("{:.3f}".format(time.time()-t0)))
    return

readandwrite_delta()