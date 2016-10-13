import pickle
import json
from getAllFiles import getPathRelative


def writeToFilePickle(filePath,data,rel=False):
    '''Writes all 'data' to file 'filePath'.
    If 'rel=True' then path is relative to cwd'''
    if rel:
        filePath = getPathRelative(filePath)
    try:
        pickle.dump(data,open(filePath,'wb'))
        return True
    except Exception as e:
        print(str(x))

def getFromFilePickle(filePath,rel=False):
    '''Returns all data from file 'filePath'.
    if 'rel=True' then path is relative to cwd'''
    if rel:
        filePath = getPathRelative(filePath)
    try:
        return pickle.load(open(filePath,'rb'))
    except Exception as e:
        print(str(e))

def writeToFile(filePath,data,rel=False):
    if rel:
        filePath = getPathRelative(filePath)
    try:
        with open(filePath,'w') as file:
            json.dump(data,file)
            return True
    except Exception as e:
        print(str(e))

def getFromFile(filePath,rel=False):
    if rel:
        filePath = getPathRelative(filePath)
    
    with open(filePath,'r') as file:
        return json.load(file)










        
    

