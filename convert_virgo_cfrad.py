#Raydel Abreu CM2ESP 11/06/2020
#Use it for convert from VIRGO file format into CFRAD format
from numpy import loadtxt
import numpy as np

#FFT bins per scan line in source
fftBins = 2048

#File Input Configuration
firstFile = 15
lastFile = 235
Increment = 5

#How many lines to average (use 1 for none)
vertInt=1

#List that contains data
lines = list()

#Read files
for f in range(firstFile,lastFile,Increment):
    sourceFile = 's'+str(f)+".txt"
    #Read File into list of scans
    lines.append(loadtxt(sourceFile, comments="#", delimiter="\n\n\r", unpack=False))

#Number of scan in the file
numScan = len(lines)

#Empty list for averaged scans
outScans = list()

#Range formatting. Required to keep values inside the accepted CFRAD levels
minVal=np.min(lines)
if minVal < 0:
   minVal=minVal*(-1.0)
lines+=(minVal+.01)
maxVal=np.max(lines)
#Define top level
topLevel=2.0
multiplier=topLevel/maxVal
lines*=multiplier
#print np.min(lines)
#print np.max(lines)

#Average scans if needed. Otherwise just save as it is
for i in range(0,numScan,vertInt):
    if i+vertInt <= numScan:
       scanAvg = np.zeros((fftBins))
       avgFrom = i
       avgTo = i+vertInt
       for sets in range(avgFrom,avgTo):
           scanAvg=scanAvg+lines[sets]
       scanAvg=scanAvg/(vertInt)
       removeBias = [x+(minVal) for x in scanAvg]
       outScans.append(removeBias)

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

