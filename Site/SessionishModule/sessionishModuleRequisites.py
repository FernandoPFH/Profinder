from os import path
import json
from time import asctime,localtime,time
from random import randint

sessionFilesPath = "./SessionishFiles"
sessionMasterFilePath = "./SessionishFiles/MasterInfo.json"

baseCaractheres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
clientSessionIdLength = 20

def createMasterFileIfNotExists():
    if not path.exists(sessionMasterFilePath):
        with open(sessionMasterFilePath,"w") as file:
            file.write(json.dumps({}))

def updateMasterFile(clientSessionId,lastRequested=False,lastUpdated=False):
    with open(sessionMasterFilePath,"r+") as file:

        masterFileJSON = json.loads(file.read())

        if not lastRequested:
            lastRequested = masterFileJSON[clientSessionId]["lastRequested"]

        if not lastUpdated:
            lastUpdated = masterFileJSON[clientSessionId]["lastUpdated"]


        masterFileJSON[clientSessionId] = {
            "lastRequested":lastRequested,
            "lastUpdated":lastUpdated
        }

        file.seek(0)
        file.write(json.dumps(masterFileJSON))
        file.truncate()

def createSessionishFile(clientSessionId,clientAdress):
    fileInfos = {
        "clientAdress": clientAdress,
        "lastRequested": asctime(localtime(time())),
        "lastUpdated": asctime(localtime(time())),
        "data": {}
    }

    with open(path.join(sessionFilesPath,clientSessionId),"w") as file:
        file.write(json.dumps(fileInfos))

def createFileThatNotExist():
    creatingNameThatNotExist = True

    while creatingNameThatNotExist:
        clientSessionId = ""
        for turn in range(clientSessionIdLength):
            clientSessionId += baseCaractheres[randint(0,len(baseCaractheres)-1)]

        if not path.exists(path.join(sessionFilesPath,clientSessionId)):
            creatingNameThatNotExist = False

    return clientSessionId

def updateRequestInfo(clientSessionId):
    with open(path.join(sessionFilesPath,clientSessionId),"r+") as file:
        sessionishJSON = json.loads(file.read())
        sessionishJSON["lastRequested"] = asctime(localtime(time()))

        file.seek(0)
        file.write(json.dumps(sessionishJSON))
        file.truncate()

    updateMasterFile(clientSessionId=clientSessionId,lastRequested=asctime(localtime(time())),lastUpdated=False)

def requestSessionishData(clientSessionId,keyNames):
    updateRequestInfo(clientSessionId)

    with open(path.join(sessionFilesPath,clientSessionId),"r") as file:
        sessionishJSON = json.loads(file.read())


    if type(keyNames) == type(str()):
        valuesOfTheKeys = [{keyNames:sessionishJSON["data"][keyNames]}]

    elif type(keyNames) == type(list()):
        valuesOfTheKeys = []

        for keyName in keyNames:
            valuesOfTheKeys.append({keyName:sessionishJSON["data"][keyName]})

    return valuesOfTheKeys

def updateUpdateInfo(clientSessionId):
    with open(path.join(sessionFilesPath,clientSessionId),"r+") as file:
        sessionishJSON = json.loads(file.read())
        sessionishJSON["lastUpdated"] = asctime(localtime(time()))

        file.seek(0)
        file.write(json.dumps(sessionishJSON))
        file.truncate()

    updateMasterFile(clientSessionId=clientSessionId,lastRequested=False,lastUpdated=asctime(localtime(time())))

def updateSessionishData(clientSessionId,valuesToUpdate):
    updateUpdateInfo(clientSessionId)

    with open(path.join(sessionFilesPath,clientSessionId),"r+") as file:
        sessionishJSON = json.loads(file.read())

        file.write(json.dumps(sessionishJSON))

        for keyToUpdate,valueToUpdate in valuesToUpdate.items():
            sessionishJSON["data"][keyToUpdate] = valueToUpdate

        file.seek(0)
        file.write(json.dumps(sessionishJSON))
        file.truncate()

def clientAdressMatchSessionishAdress(clientSessionId,clientAdress):
    with open(path.join(sessionFilesPath,clientSessionId),"r") as file:
        sessionishJSON = json.loads(file.read())

    return sessionishJSON["clientAdress"] == clientAdress

def sessionishFileExist(clientSessionId):
    return path.exists(path.join(sessionFilesPath,clientSessionId))