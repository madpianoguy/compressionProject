import json


def getEncode(toEncode):
    return json.dumps(toEncode).encode('utf-8')

def getDecode(toDecode):
    return json.loads(toDecode.decode('utf-8'))

