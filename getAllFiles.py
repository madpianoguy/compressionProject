import os
import shutil
import glob

def getPathRelative(path):
    '''Returns the complete path, joining the cwd with the 'path'''
    return os.path.join(os.getcwd(),path)    

def returnFileList(startPath):
    '''Returns a list with file paths for all the
    files inside 'startPath' recursively.'''
    path = str(startPath)+'/**/*.*'
    return [x for x in glob.iglob(path,recursive=True)]

def returnFileList1(startPath,fromCWD=True):
    '''Broken'''
    if fromCWD:
        startPath = os.path.join(os.getcwd(),startPath)
    fileList = []
    for root, directories, filenames in os.walk(startPath):
        for filename in filenames:
            try:
                fileList.append(os.path.join(root,filename))
                #print(os.path.join(root,filename))
            except:
                pass
    return fileList

def removeDirectory(path=None, relPath=None):
    '''Removes directory recursively at 'path'.
    'relPath = True' sets the path relative to CWD'''
    if relPath:
        path = os.path.join(os.getcwd(),relPath)
    shutil.rmtree(path)

def removeFile(path=None, relPath=None):
    '''Removes file at path specified.
    'relPath=True' sets the path relative to CWD'''
    if relPath:
        path = os.path.join(os.getcwd(),relPath)
    os.remove(path)

def returnFileListSize(startPath):
    '''Defunct Function'''
    fileList = []
    count=0
    for root, directories, filenames in os.walk(startPath):
        for filename in filenames:
            filePath = os.path.join(root,filename)
            fileSize = os.path.getsize(filePath)
            join = [filePath,fileSize]
            fileList.append(join)
            count+=1
            if count %1000 == 0:
                print(count)
    return fileList,count



if __name__ == '__main__':
    print(len(returnFileList('C:')))
    #x = returnFileList1('C:',False)
    #print(len(x))
    #for y in range(0,len(x),5):
    #    print(x[y])
