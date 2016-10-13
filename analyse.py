
import os
import datetime
import time as Time

def getFileSize(filePath):
    return os.path.getsize(filePath)

def getFileType(filePath):
    index=1
    for c in filePath:
        if c == '.':
            break
        else:
            index += 1
    return filePath[index:]

def getCompRatio(initialSize,finalSize,dp=3):
    return round((finalSize/initialSize),dp)

def getCurDate1():
    time =  datetime.datetime.now()
    return str(time)

def getCurDate():
    return Time.time()

def roundTime(time):
    pass

def calcRelTime(time,relTime):
    return round((time/relTime),6)

def getFileName(filePath):
    revName=''
    for char in filePath[::-1]:
        if char != '\\':
            revName = char + revName
        else:
            return revName


def initialAnalyseList(fileList,path=True,size=True,fileType=True):
    updatedList = []
    for file in fileList:
        fileInfo = {}
        if path:
            fileInfo['filePath'] = file
        if size:
            fileInfo['initialSize'] = getFileSize(file)
        if fileType:
            fileInfo['fileType'] = getFileType(file)

        updatedList.append(fileInfo)

    return updatedList

def initialAnalyse(filePath,fileName=True,size=True,fileType=True):
    fileInfo = {}
    fileInfo['filePath'] = filePath
    if fileName:
        fileInfo['fileName'] = getFileName(filePath)
    if size:
        fileInfo['initialSize'] = getFileSize(filePath)
    if fileType:
        fileInfo['fileType'] = getFileType(filePath)

    return fileInfo

def afterAnalyse(fileInfo,compressedPath,timeTaken=None,compPath=True,size=True,
                 compType=True,ratio=True,date=True,relTime=True):
    if compPath:
        fileInfo['compPath'] = compressedPath
    if size:
        fileInfo['compSize'] = getFileSize(compressedPath)
    if compType:
        fileInfo['compType'] = getFileType(compressedPath)
    if ratio:
        try:
            fileInfo['ratio'] = getCompRatio(fileInfo['initialSize'],fileInfo['compSize'])
        except:
            fileInfo['ratio'] = 1
    if date:
        fileInfo['date'] = round(getCurDate())
    if timeTaken:
        fileInfo['time'] = float(str(timeTaken)[:5])
    if relTime:
        fileInfo['relTime'] = 1
    return fileInfo

if __name__ == '__main__':
    pass

            
