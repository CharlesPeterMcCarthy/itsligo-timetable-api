import json
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err
import helpers.datetime as dt

def Handler(event, context):
    data = json.loads(event['body'])
    return CheckLoginDetails(data) if fnc.ContainsAllData(data, ('username', 'password')) else fnc.ErrorResponse(err.MISSING_DETAILS)

def CheckLoginDetails(data):
    username = data['username'].lower()

    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.get_item(Key={'username': username})
    except: return fnc.ErrorResponse(err.DB_QU)

    if 'Item' in res: res = res['Item']
    else: return fnc.ErrorResponse(err.INVALID_USERNAME)

    if not res['verified']: return fnc.ErrorResponse(err.UNVERIFIED_USER)

    if 'password' in res and fnc.VerifyPassword(data['password'], res['password']): del res['password']
    else: return fnc.ErrorResponse(err.WRONG_PASSWORD)

    authToken = fnc.GenerateAuthToken()
    authRes = fnc.UpdateAuthToken(username, authToken)

    UpdateLoginDatetime(username)

    return fnc.SuccessResponse({'user': res, 'authToken': authToken}) if 'updated' in authRes and authRes['updated'] else fnc.ErrorResponse(authRes)

def UpdateLoginDatetime(username):
    loginAt = dt.GetCurrentDatetime()

    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.update_item(
            Key={'username': username},
            UpdateExpression="set #t.#l = :d",
            ExpressionAttributeNames={'#t': 'times', '#l': 'lastLogin'},
            ExpressionAttributeValues={':d': loginAt},
            ReturnValues="NONE"
        )
    except:
        res = err.DB_UP
    return res
