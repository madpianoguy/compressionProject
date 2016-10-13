from subprocess import call

import os

CURRENT = os.getcwd()
COMPRESSIONTYPES = ['zip']
COMPRESSIONLEVELS = [1,3,5,7,9]
TOCOMPRESS = CURRENT+'\MediaToCompress'
COMPRESSED = CURRENT+'\MediaCompressed'
FILES = os.listdir(TOCOMPRESS)

def compressIndividual(compType,level):
    for file in FILES:
        file=str(file)
        command = ('7za a '+ '-mx' + str(level) + ' ' + COMPRESSED+'\\' +
                   file[:-4]+ 'Compressed.' + compType + ' ' +
                   TOCOMPRESS+'\\' + file)

        call(command,shell=True)

def compressTogether(compType,level):
    command = ('7za a '+ '-mx' + str(level) + ' ' + COMPRESSED +'\\'
               + str(level)+'Compressed.'+ compType + ' ' + TOCOMPRESS)

    call(command, shell=True)

def testAllRatio(compType,folderType):
    if folderType == 1:
        for level in COMPRESSIONLEVELS:
            print('Starting Level:', str(level))
            compressIndividual(compType,level)
    elif folderType == 2:
        for level in COMPRESSIONLEVELS:
            print('Starting Level:', str(level))
            compressTogether(compType,level)

if __name__ == '__main__':
    print(FILES)
    testAllRatio('zip', 2)
