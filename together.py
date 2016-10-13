import createDatabase
from together1 import manageAll
from getAllFiles import returnFileList,removeFile,getPathRelative
from compressionCommands import compressSpecific
from analyse import initialAnalyse,afterAnalyse
from savingProgress import writeToFile,getFromFile
from createDatabase import checkIfExists,getDataWhere,displayResults,getNumberItems
from createDatabase import insertDataDict,resetDatabase,getData
from clientCompress import connect,sendDict,connectSendList
from clientCompress import getBestCompClient
import time
import os

DATABASE = 'results.db'
TABLE = 'results'

COMPTYPES = ['zip','cab','arj','tar','cpio','rpm','deb']#,'gzip','bzip2']
COMPTYPESOTHER = ['gzip','bzip2']

def workThroughAllReturnList(fileListPath,rel=False,chunk=100):
    myDataList = []
    print('retrieving File List')
    fileList = getFromFile(fileListPath,rel)
    print('Analysing Files')
    for x in range(len(fileList[:chunk])):
        file = fileList.pop(0)
        print(file)
        for comp in COMPTYPES:
            try:
                myDataList.append(analyseTidy(file,comp,9))
                #analyseFile(file,comp,9)
            except Exception as e:
                print(str(e))
    print('saving Results')
    writeToFile(fileListPath,fileList)
    print('Finished')
    if len(fileList) > 0:
        return True,myDataList
    else:
        return False,myDataList

def sendListToServer(addr,port,dataList):
    try:
        for data in dataList:
            myConn = connect(addr,port)
            sendDict(myConn,data)
            time.sleep(1)
            break
        sendDict(myConn,'endofdata')
        return True
    except Exception as e:
        print(str(e))
        return False




def analyseTidy(filePath,compType,level):
    '''Analyses file at 'filePath' with compression 'compType' performed
    with 'level' of compression (9=high,1=low).
    Deletes compressed file after compression.'''
    fileInfo = initialAnalyse(filePath)
    startTime = time.clock()
    compPath = compressSpecific(filePath,compType,level)
    endTime = time.clock()
    totalTime = endTime-startTime
    #print(compPath)
    fileInfo = afterAnalyse(fileInfo,compPath,timeTaken=totalTime)
    #print('hi3')
    removeFile(path=compPath)

    return fileInfo

def insertIntoDB(fileInfo,dbName):
    '''Inserts 'fileInfo' into database "dbName"'''
    insertDataDict(dbName,fileInfo)

def setRelTime():
    '''Defunct'''
    fileInfo = analyseTidy((os.path.join(os.getcwd(),'words.txt')),'zip',9)
    return fileInfo['time']


def analyseFile(filePath,compType,level):
    '''Analyses file and inserts results into database'''
    fileInfo = analyseTidy(filePath,compType,level)
    #return True
    insertIntoDB(fileInfo,DATABASE)

def saveAllFileList(fileList,path):
    '''Saves 'fileList' to file 'path'.'''
    writeToFile(path,fileList,True)

def getSaveFileList(savePath,startPath,rel=False,relSave=False):
    if rel:
        startPath = getPathRelative(startPath)        
    fileList = returnFileList(startPath)
    writeToFile(savePath,fileList,relSave)

def workThroughAll(fileListPath,rel=False,chunk=100):
    print('retrieving File List')
    fileList = getFromFile(fileListPath,rel)
    #fileList = returnFileList(getPathRelative('MediaToCompress'))
    print('Analysing Files')
    for x in range(len(fileList[:chunk])):
        file = fileList.pop(0)
        print(file)
        for comp in COMPTYPES:
            try:
                analyseFile(file,comp,9)
            except:
                pass
    print('saving Results')
    writeToFile(fileListPath,fileList)
    print('Finished')
    if len(fileList) > 0:
        return True
    else:
        return False



def timeManage(fileListPath,tm,rel=False,):
    endTime = time.time() + int(tm)
    cont = True
    while time.time() < endTime and cont:
        cont = workThroughAll(fileListPath,rel,tm)


def timeManageSendToServer(fileListPath,tm,rel=False):
    numFiles = tm/5
    if numFiles < 1:
        numFiles = 1
    else:
        numFiles = round(numFiles)
    endTime = time.time() + int(tm)
    cont = True
    notSent = []
    count = 0
    while time.time() < endTime and cont:
        count +=1
        cont,DataList = workThroughAllReturnList(fileListPath,rel,numFiles)
        sent = connectSendList('localhost',8089,DataList)
        if not sent:
            for item in DataList:
                notSent.append(item)
        tN = time.time()
        timeTaken = tm-(endTime-tN)
        averageTimeTaken = timeTaken/count
        print(averageTimeTaken)
        if endTime-tN-averageTimeTaken < 0:
            #print('quitting')
            break
    print(len(notSent),'results not sent to server')
    print(count*numFiles,'items processed')
    print(round(time.time() - endTime),'seconds over target time')
    print(round(timeTaken),tm,'seconds taken')




    

if __name__ == '__main__':
    resetDatabase(DATABASE)
    getSaveFileList('mySaveFileList.json','C:/Program Files (x86)/Audacity')
    timeManageSendToServer('mySaveFileList.json',64,True)
    #timeManage('mySaveFileList.json',420,True)
    #fileList = getFromFile('mySaveFileList.json',True)
    #print(len(fileList))
    #workThroughAll('mySaveFileList.json',True,10)
    #saveAllFileList(returnFileList('C:'),'fileList.txt')
    #resetDatabase(DATABASE)
    #getData(DATABASE)
