      import csv

def writehelper(i, writein):
    filename = 'ProcessedData/pbpb_' + str(i) + '.csv'
    f = open(filename, 'w')
    writer = csv.writer(f)
    writer.writerows(writein)
    f.close()


def readandwrite(): #this read line from PbPb file, and recognize event start and end. return rows
    with open('Pbpb_2015.txt') as f:
        eventindex = -1
        writeinrows = []
        while True:
            thisline = f.readline()
            if "Number" not in thisline and not thisline.__eq__('\n') and not thisline.__eq__(''):
                writeinrows.append(list(thisline.split()))
            if "Event" in thisline:
                eventindex += 1
                if eventindex != 0:
                    writehelper(eventindex-1, writeinrows)
                    writeinrows = []
            if not thisline:
                writehelper(eventindex, writeinrows)
                break
        # writehelper(eventindex-1, writeinrows)
    return

readandwrite()