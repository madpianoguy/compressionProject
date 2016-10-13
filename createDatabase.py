import sqlite3 as lite
from getAllFiles import removeFile

print(lite.version)

def connectDB(name):
    conn = lite.connect(name)
    cur = conn.cursor()
    return conn, cur

def create():
    try:
        conn = lite.connect('test.db')
        cur = conn.cursor()
    except:
        print('Could Not Oblige')

def createTable(name):
    conn, cur = connectDB(name)

    conn.execute('''CREATE TABLE results
            (ID INT PRIMARY KEY,
            FILENAME        CHAR(10),
            FILETYPE        CHAR(10),
            COMPTYPE        CHAR(10),
            FILEPATH        STRING,
            COMPPATH        STRING,
            ORIGINALSIZE    INT,
            FINALSIZE       INT,
            RELTIME         REAL,
            RATIO           REAL,
            TIMETAKEN       REAL,
            DATE            INT);''')
    conn.close()

def resetDatabase(dbName):
    text = ('DELETE ALL DATA IN ' + dbName.upper() + ' (Y/n)')
    answer = input(text)
    if answer == 'Y':
        print('Deleting')
        removeFile(relPath=dbName)
        createTable(dbName)

def insertData(dbName,fileType,originalSize,finalSize,ratio,timeTaken,date):
    conn,cur = connectDB(dbName)

    conn.execute("INSERT INTO RESULTS (TYPE,ORIGINALSIZE,FINALSIZE,RATIO,TIMETAKEN,DATE) \
            VALUES (?,?,?,?,?,?)",
                 (fileType,originalSize,finalSize,ratio,timeTaken,date))

    conn.commit()
    conn.close()

def insertDataDict(dbName,fileInfo):
    conn,cur = connectDB(dbName)

    conn.execute("INSERT INTO RESULTS (FILENAME, FILETYPE, FILEPATH, ORIGINALSIZE,\
            COMPTYPE, COMPPATH, FINALSIZE, RATIO, RELTIME, TIMETAKEN, DATE)\
            VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                 (fileInfo['fileName'],fileInfo['fileType'],fileInfo['filePath'],
                  fileInfo['initialSize'],fileInfo['compType'],
                  fileInfo['compPath'],fileInfo['compSize'],
                  fileInfo['ratio'],fileInfo['relTime'],fileInfo['time'],
                  fileInfo['date']))
    conn.commit()
    conn.close()



def getData(tableName):
    conn,cur = connectDB(tableName)

    results = conn.execute("SELECT ROWID, FILENAME, FILETYPE, ORIGINALSIZE,\
            COMPTYPE, FINALSIZE, RATIO, \
            TIMETAKEN, DATE FROM RESULTS")
    for row in results:
        print(row)

def getDataWhere(dbName,tableName,what,where=False,order=False):
    conn,cur = connectDB(dbName)

    command = "SELECT " + what + " FROM " + tableName
    if where:
        command = command + " WHERE " + where
    if order:
        command = command + ' ORDER BY ' + order

    results = conn.execute(command)

    return results

def displayResults(resultsList):
    try:
        for row in resultsList:
            print(row)
    except Exception as e:
        print(str(e))
    

def checkIfExists1(dbName,table,what):
    conn,cur = connectDB(dbName)

    command = 'SELECT EXISTS(SELECT 1 FROM ' + table + ' WHERE '+ what

    cur.execute(command)

    if cur.fetchnone():
        return True
    else:
        return False

def checkIfExists(dbName,table,what):

    results = getDataWhere(dbName,table,'FILEPATH',what)
    count = 0
    for row in results:
        count +=1
        if count != 0:
            return True
    return False

def getNumberItems(dbName,table):
    conn,cur = connectDB(dbName)
    command = 'SELECT COUNT(*) FROM '+table
    someStr = ''
    number = ''
    x = cur.execute(command)
    for row in x:
        someStr= someStr+str(row)
    for char in someStr:
        try:
            int(char)%1
            number = number+ char
        except:
            pass
    return int(number)



if __name__ == '__main__':
    DATABASE = 'results.db'
    TABLE = 'RESULTS'
    #resetDatabase(DATABASE)
    #what = 'FILEPATH = "C:alpha150916.zip"'
    #getNumberItems(DATABASE,TABLE)
    #print(checkIfExists(DATABASE,TABLE,what))
    #createTable(DATABASE)
    #dataList = ['WAV','7z',300,100,0.33,25,12345678]
    #insertData(DATABASE,*dataList)
    #getData(DATABASE)
