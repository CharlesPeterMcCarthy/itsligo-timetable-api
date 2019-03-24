import json
import datetime
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def Handler(event, context):
    data = json.loads(event['body'])
    return CheckLoginDetails(data) if fnc.ContainsAllData(data, ('studentID', 'password')) else fnc.ErrorResponse(err.MISSING_DETAILS)

def CheckLoginDetails(data):
    studentID = data['studentID'].upper()

    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.get_item(Key={ 'studentID': studentID })
    except: return fnc.ErrorResponse(err.DB_QU)

    if 'Item' in res: res = res['Item']
    else: return fnc.ErrorResponse(err.INVALID_STUDENTID)

    if not res['verified']: return fnc.ErrorResponse(err.UNVERIFIED_USER)

    if 'password' in res and fnc.VerifyPassword(data['password'], res['password']): del res['password']
    else: return fnc.ErrorResponse(err.WRONG_PASSWORD)

    authToken = fnc.GenerateAuthToken()
    authRes = fnc.UpdateAuthToken(studentID, authToken)

    UpdateLoginDatetime(studentID)

    return fnc.SuccessResponse({ 'user': res, 'authToken': authToken }) if 'updated' in authRes and authRes['updated'] else fnc.ErrorResponse(authRes)

def UpdateLoginDatetime(studentID):
    loginAt = datetime.datetime.now().isoformat()

    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.update_item(
            Key={ 'studentID': studentID },
            UpdateExpression="set #t.#l = :d",
            ExpressionAttributeNames={ '#t': 'times', '#l': 'lastLogin' },
            ExpressionAttributeValues={ ':d': loginAt },
            ReturnValues="NONE"
        )
    except:
        res = err.DB_UP
    return res
