import json
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def Handler(event, context):
    data = json.loads(event['body'])
    return CheckLoginDetails(data) if all(d in data for d in ('studentID', 'password')) else fnc.ErrorResponse(err.MISSING_DETAILS)

def CheckLoginDetails(data):
    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.get_item(Key={ 'StudentID': data['studentID'] })
    except:
        return fnc.ErrorResponse(err.UNKNOWN)

    if 'Item' in res:
        res = res['Item']
    else:
        return fnc.ErrorResponse(err.INVALID_STUDENTID)

    if 'Password' in res:
        if fnc.VerifyPassword(data['password'], res['Password']):
            del res['Password']
        else:
            return fnc.ErrorResponse(err.WRONG_PASSWORD)

    return fnc.SuccessResponse({ 'user': res, 'Access-Token': fnc.GenerateAccessToken() })
