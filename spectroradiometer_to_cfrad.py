from numpy import loadtxt
import numpy as np

#FFT bins per scan line in source
fftBins = 2048

#Exclude columns at first
ignoreCol = 9

#How many scans to average into a single line
vertInt = 5

#Source file name and path
sourceFile = "h120200609-0-spec.csv"
#Read File into list of scans
lines = loadtxt(sourceFile, comments="#", delimiter=",", unpack=False, usecols=range(ignoreCol,ignoreCol+fftBins))

#####
#Secondary file for merge if needed
secondFile = "h120200610-0-spec.csv"
secondLines = loadtxt(secondFile, comments="#", delimiter=",", unpack=False, usecols=range(ignoreCol,ignoreCol+fftBins))
#Append second file
lines= np.concatenate((lines,secondLines))
#####


#Number of scan in the file
numScan = len(lines)

#Empty list for averaged scans
outScans = list()

#Average scans
for i in range(0,numScan,vertInt):
    if i+vertInt <= numScan:
       scanAvg = np.zeros((fftBins))
       avgFrom = i
       avgTo = i+vertInt
       for sets in range(avgFrom,avgTo):
           scanAvg=scanAvg+lines[sets]
       scanAvg=scanAvg/(vertInt)
       #Now linearize
       linearScan = [pow(10,x/20.0) for x in scanAvg]
       #print linearScan
       outScans.append(linearScan)

#now Save to file
print len(outScans)-1
for j in range(len(outScans)):
    f = open('nrad-'+str(j)+'.txt', 'w')
    for k in range(len(outScans[j])):
        f.write(str(outScans[j][k])+'\r\n')
    f.close()

#ready
print"done"
exit()

