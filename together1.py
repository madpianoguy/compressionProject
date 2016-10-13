
import createDatabase
from getAllFiles import returnFileList,removeFile
from compressionCommands import compressSpecific
from analyse import initialAnalyse,afterAnalyse
from savingProgress import writeToFile,getFromFile
from createDatabase import checkIfExists,getDataWhere,displayResults,getNumberItems
from createDatabase import insertDataDict
import time
import os

DATABASE = 'results.db'
TABLE = 'results'

COMPTYPES = ['zip','cab','arj','gzip','bzip2','tar','cpio','rpm','deb']

def analyseTidy(filePath,compType,level):
    '''Analyses file at 'filePath' with compression 'compType' performed
    with 'level' of compression (9=high,1=low).
    Deletes compressed file after compression.'''
    fileInfo = initialAnalyse(filePath)
    startTime = time.clock()
    compPath = compressSpecific(filePath,compType,level)
    print('hi')
    endTime = time.clock()
    totalTime = endTime-startTime
    print(compPath)
    fileInfo = afterAnalyse(fileInfo,compPath,timeTaken=totalTime)
    print('hi3')
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
    insertIntoDB(fileInfo,DATABASE)

def saveAllFileList(fileList,path):
    '''Saves 'fileList' to file 'path'.'''
    writeToFile(path,fileList,True)

def workThroughAll(fileListPath,rel=False,chunk=100):
    fileList = getFromFile(fileListPath,rel)
    for x in fileList[:chunk]:
        file = fileList.pop(0)
        for comp in COMPTYPES:
            print(file)
            analyseFile(file,'9',comp)
            break
    writeToFile(fileListPath,fileList,rel)


def manageAll():
    '''Analyses every single file on computer and stores data in database'''
    initialStart = getNumberItems(DATABASE,TABLE)
    print(initialStart)
    errors = 0
    sTime = time.clock()
    fileList = returnFileList('C:',False)
    total = (len(fileList)*9)
    print('Finished Filelist with', len(fileList),
          'Items',total,'Compressions To Perform')
    for file in fileList:
        whats = 'FILEPATH = "'+ str(file)+'"'
        if not checkIfExists(DATABASE, TABLE, whats):
            for comp in COMPTYPES:
                try:
                    analyseFile(file,comp,9)
                    initialStart+=1
                    #print('C',initialStart)
                except Exception as e:
                    errors += 1
                    print(str(e))
                    #print('E',str(e))
                totalDone = initialStart+errors
                pD = round(totalDone/total,2)
                pDd = pD
                pDS = ''
                for x in range(20):
                    if pDd - 0.05 >= 0:
                        pDd -= 0.05
                        pDS = pDS + '*'
                    else:
                        pDS = pDS + '#'
                
                if (initialStart+errors) % 100 == 0:
                    print(str(pD)[2:],'%', pDS)
                    #print('T',initialStart+errors,'E',errors,'C',initialStart)
    print(time.clock()-sTime)

if __name__ == '__main__':
    manageAll()




