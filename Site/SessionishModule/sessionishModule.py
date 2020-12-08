from SessionishModule.sessionishModuleRequisites import createMasterFileIfNotExists,createFileThatNotExist,createSessionishFile,updateMasterFile,sessionishFileExist,clientAdressMatchSessionishAdress,requestSessionishData,updateSessionishData

from time import asctime,localtime,time

createMasterFileIfNotExists()

def newSessionishStart(clientAdress):
    clientSessionId = createFileThatNotExist()

    createSessionishFile(clientSessionId,clientAdress)

    updateMasterFile(clientSessionId=clientSessionId,lastRequested=asctime(localtime(time())),lastUpdated=asctime(localtime(time())))

    return clientSessionId

def newSessionishRequest(clientSessionId,clientAdress,keyNames):
    if sessionishFileExist(clientSessionId):
        if clientAdressMatchSessionishAdress(clientSessionId,clientAdress):
            response = requestSessionishData(clientSessionId,keyNames)
        else:
            response = "ClientAdressNotMatchSessionishFile"
    else:
        response = "SessionishFileNotExists"

    return response

def newSessionishUpdate(clientSessionId,clientAdress,valuesToUpdate):
    if sessionishFileExist(clientSessionId):
        if clientAdressMatchSessionishAdress(clientSessionId,clientAdress):
            response = updateSessionishData(clientSessionId,valuesToUpdate)
        else:
            response = "ClientAdressNotMatchSessionishFile"
    else:
        response = "SessionishFileNotExists"