import socket
import json
import time
from encodeJson import getEncode,getDecode

enc = 'utf-8'

def connect(addr,port):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((addr, port))
    return clientsocket

def sendDict(connection,dataDict):
    try:
        data = json.dumps(dataDict).encode('utf-8')
        connection.send(data)
    except Exception as e:
        return e

def sendList(connection,aList):
    aList.append('endofalldata')
    for item in aList:
        #print('Sending',item)
        sendDict(connection,item)
        connection.recv(1024)
        #print('False')
        
    #sendDict(connection,'endofalldata')

def connectSendList(addr,port,someList):
    try:
        sendList(connect(addr,port),someList)
        return True
    except Exception as e:
        print(str(e))
        return False

def getDataFromServer(addr,port,data):
    conn = connect(addr,port)
    conn.sendall(getEncode(data))
    msg = conn.recv(4096)
    if len(msg) > 0:
        data = getDecode(msg)
        try:
            return data.pop(0)
        except:
            return []

def getBestCompClient(addr,port,details):

    print(getDataFromServer(addr,port,details)) 
    

if __name__=='__main__':
    myList = [str(x) for x in range(0,100,2)]
    #conn = connect('localhost',8089)
    #sendList(conn,myList)
    #sendDict(conn,{'Hi':'Bye'})
    #connectSendList('localhost',8089,myList)
    getBestCompClient('localhost',8091,{'fileType':'png','initialSize':500})
