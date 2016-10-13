from analyse import initialAnalyse
from createDatabase import getDataWhere,displayResults
from getAllFiles import returnFileList
from clientCompress import getDataFromServer

DATABASE = 'resultsOLD.db'
TABLE = 'RESULTS'


def findBestComp(database,table,details,sort,num,path=None):

    if not path:
        path = returnFileList('testingComp')
    else:
        path = returnFileList(path,False)

    #details = initialAnalyse(path[0])
    size = details['initialSize']
    size += round(size/10)
    whereDetails = ('FILETYPE = "'+ details['fileType']+
                    '" AND ORIGINALSIZE < '+ str(size))
    whereDetails2 = 'FILETYPE = "mp3"'

    whereDetails3 = ('FILETYPE = "'+ details['fileType']+
                    '" AND ORIGINALSIZE < '+ str(size*2))
    sortDetails = sort+' ASC'
    print('Where details:',whereDetails)
    dbResults = getDataWhere(database,table,
                             'RATIO,ORIGINALSIZE,FINALSIZE,TIMETAKEN,COMPTYPE',
                             whereDetails, sortDetails)
    count1 = 0
    aList=[]
    for item in dbResults:
        print('item',item)
        bList = []
        for xtem in item:
           bList.append(xtem)
        aList.append(bList)
        count1+=1
        if count1 >= num or len(aList) == len(bList):
            return(aList)

def getBestComp(database,table,details,sort,num,path=None):
    aList = findBestComp(database,table,details,sort,num)
    displayResults(aList)

   


if __name__ == '__main__':
    getBestComp(DATABASE,TABLE,{'fileType':'txt','initialSize':500},'RATIO',10)
