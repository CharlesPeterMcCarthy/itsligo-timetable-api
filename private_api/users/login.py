import json
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def Handler(event, context):
    data = json.loads(event['body'])
    return CheckLoginDetails(data) if fnc.ContainsAllData(data, ('studentID', 'password')) else fnc.ErrorResponse(err.MISSING_DETAILS)

def CheckLoginDetails(data):
    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.get_item(Key={ 'StudentID': data['studentID'] })
    except: return fnc.ErrorResponse(err.DB_QU)

    if 'Item' in res: res = res['Item']
    else: return fnc.ErrorResponse(err.INVALID_STUDENTID)

    if not res['Verified']: return fnc.ErrorResponse(err.UNVERIFIED_USER)

    if 'Password' in res and fnc.VerifyPassword(data['password'], res['Password']): del res['Password']
    else: return fnc.ErrorResponse(err.WRONG_PASSWORD)

    authToken = fnc.GenerateAuthToken()
    authRes = fnc.UpdateAuthToken(data['studentID'], authToken)

    return fnc.SuccessResponse({ 'user': res, 'Access-Token': authToken }) if 'Updated' in authRes and authRes['Updated'] else fnc.ErrorResponse(authRes)
