import socket
import json
from createDatabase import insertDataDict
from chooseBest import findBestComp
from multiprocessing import Process
from encodeJson import getEncode,getDecode
import time

DATABASE = 'results.db'
TABLE = 'RESULTS'
GETADDR = 'localhost'
GETPORT = 8089
SENDADDR = 'localhost'
SENDPORT = 8091

def runRecieveDataServer(addr,port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((addr,port))
    serversocket.listen(5)
    while True:
        print('RDS - Waiting for connection')
        connection, address = serversocket.accept()
        print('RDS - Connection Made')
        while True:
            buf = connection.recv(4096)
            if len(buf) > 0:
                msg = buf.decode('utf-8')
                #print(msg)
                data = json.loads(msg)
                if data == 'endofalldata':
                    print('RDS - Ending')
                    connection.close()
                    break
                print('RDS - Inserting Data')
                #print(data['compType'])
                insertDataDict(DATABASE,data)
                #print('completed')
                connection.sendall(b'True')

def runSendDataServer(addr,port):
    while True:
        try:
            print('SDS - Starting Server')
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.bind((addr,port))
            s.listen(5)
            while True:
                print('SDS - Waiting for connection')
                connection,address = s.accept()
                print('SDS - Connection made at',connection,address)
                buf = connection.recv(4096)
                if len(buf) > 0:
                    msg = getDecode(buf)
                    print('SDS - Request recieved for',msg)
                    try:
                        details = findBestComp(DATABASE,TABLE,msg,'RATIO',1)
                        print('SDS - Data Retrieved')
                    except Exception as e:
                        print('SDS -',str(e))
                    connection.sendall(getEncode(details))
                    connection.close()
                    print('SDS - Connection Closed')
        except Exception as e:
            print('SDS - Error',str(e))
            print('SDS - Restarting Server')

def runBothServers(getAddr,getPort,sendAddr,sendPort):
    rS = Process(target=runRecieveDataServer,args=(getAddr,getPort))
    sS = Process(target=runSendDataServer,args=(sendAddr,sendPort))
    rS.start()
    sS.start()


    
                
        

if __name__=='__main__':
    runBothServers(GETADDR,GETPORT,SENDADDR,SENDPORT)
    #runSendDataServer('localhost',8091)
    #runRecieveDataServer('localhost',8089)
    
