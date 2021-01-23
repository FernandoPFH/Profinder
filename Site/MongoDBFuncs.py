from time import asctime,localtime,time
from random import randint

baseCaractheres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
clientSessionIdLength = 20

def createFileThatNotExist(mongoClient):
    creatingNameThatNotExist = True

    while creatingNameThatNotExist:
        clientSessionId = ""
        for turn in range(clientSessionIdLength):
            clientSessionId += baseCaractheres[randint(0,len(baseCaractheres)-1)]

        if not mongoClient["Data"]["clientsInfo"].find_one({"_id":clientSessionId}):
            creatingNameThatNotExist = False

    return clientSessionId

def createSessionishFile(mongoClient,clientSessionId,clientAdress):
    fileInfos = {
        "_id":clientSessionId,
        "clientAdress": clientAdress,
        "lastRequested": asctime(localtime(time())),
        "lastUpdated": asctime(localtime(time())),
        "data": {}
    }

    mongoClient["Data"]["clientsInfo"].insert_one(fileInfos)

def updateMasterFile(mongoClient,clientSessionId,lastRequested=False,lastUpdated=False):
    mongoCol = mongoClient["Data"]["MasterInfo"]
    queryResult = mongoCol.find_one({"_id":clientSessionId})
    if queryResult:
        if not lastRequested:
            lastRequested = queryResult["lastRequested"]

        if not lastUpdated:
            lastUpdated = queryResult["lastUpdated"]

        infoToUpdate = {
            "_id":clientSessionId,
            "lastRequested":lastRequested,
            "lastUpdated":lastUpdated
        }

        mongoCol.update_one(queryResult,{"$set":infoToUpdate})
    else:
        infoToUpdate = {
            "_id":clientSessionId,
            "lastRequested":lastRequested,
            "lastUpdated":lastUpdated
        }

        mongoCol.insert_one(infoToUpdate)

def sessionishFileExist(mongoClient,clientSessionId):
    return mongoClient["Data"]["clientsInfo"].count_documents({"_id":clientSessionId})

def clientAdressMatchSessionishAdress(mongoClient,clientSessionId,clientAdress):
    return mongoClient["Data"]["clientsInfo"].find_one({"_id":clientSessionId})["clientAdress"] == clientAdress

def updateRequestInfo(mongoClient,clientSessionId):
    mongoClient["Data"]["clientsInfo"].update_one({"_id":clientSessionId},{"$set":{"lastRequested":asctime(localtime(time()))}})

    updateMasterFile(mongoClient,clientSessionId=clientSessionId,lastRequested=asctime(localtime(time())),lastUpdated=False)

def requestSessionishData(mongoClient,clientSessionId,keyNames):
    updateRequestInfo(mongoClient,clientSessionId)

    dataFromDB = mongoClient["Data"]["clientsInfo"].find_one({"_id":clientSessionId})
    
    valuesOfTheKeys = {}

    if type(keyNames) == type(str()):
        valuesOfTheKeys[keyNames] = dataFromDB["data"][keyNames]

    elif type(keyNames) == type(list()):
        for keyName in keyNames:
            valuesOfTheKeys[keyName] = dataFromDB["data"][keyName]

    return valuesOfTheKeys

def updateUpdateInfo(mongoClient,clientSessionId):
    mongoClient["Data"]["clientsInfo"].update_one({"_id":clientSessionId},{"$set":{"lastUpdated":asctime(localtime(time()))}})

    updateMasterFile(mongoClient,clientSessionId=clientSessionId,lastRequested=False,lastUpdated=asctime(localtime(time())))

def updateSessionishData(mongoClient,clientSessionId,valuesToUpdate):
    updateUpdateInfo(mongoClient,clientSessionId)

    dataFromDB = mongoClient["Data"]["clientsInfo"].find_one({"_id":clientSessionId})
    dataUpdated = dataFromDB["data"].copy()

    for keyToUpdate,valueToUpdate in valuesToUpdate.items():
        dataUpdated[keyToUpdate] = valueToUpdate

    mongoClient["Data"]["clientsInfo"].update_one({"_id":clientSessionId},{"$set":{"data":dataUpdated}})

def newSessionishStart(mongoClient,clientAdress):
    clientSessionId = createFileThatNotExist(mongoClient)

    createSessionishFile(mongoClient,clientSessionId,clientAdress)

    updateMasterFile(mongoClient=mongoClient,clientSessionId=clientSessionId,lastRequested=asctime(localtime(time())),lastUpdated=asctime(localtime(time())))

    return clientSessionId

def newSessionishRequest(mongoClient,clientSessionId,clientAdress,keyNames):
    if sessionishFileExist(mongoClient,clientSessionId):
        if clientAdressMatchSessionishAdress(mongoClient,clientSessionId,clientAdress):
            response = requestSessionishData(mongoClient,clientSessionId,keyNames)
        else:
            response = "ClientAdressNotMatchSessionishFile"
    else:
        response = "SessionishFileNotExists"

    return response

def newSessionishUpdate(mongoClient,clientSessionId,clientAdress,valuesToUpdate):
    if sessionishFileExist(mongoClient,clientSessionId):
        if clientAdressMatchSessionishAdress(mongoClient,clientSessionId,clientAdress):
            updateSessionishData(mongoClient,clientSessionId,valuesToUpdate)
            response = True
        else:
            response = "ClientAdressNotMatchSessionishFile"
    else:
        response = "SessionishFileNotExists"

    return response