import json
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def Handler(event, context):
    data = json.loads(event['body'])
    if not fnc.ContainsAllData(data, ('authToken', 'username', 'timetableURL')): return fnc.ErrorResponse(err.MISSING_DETAILS)
    auth = fnc.AuthUser(data)
    if 'authOk' not in auth or not auth['authOk']: return fnc.ErrorResponse(auth)
    return ChangeTimetable(data)

def ChangeTimetable(data):
    username = data['username']

    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.get_item(Key={'username': username})

        if 'Item' in res:
            res = userTable.update_item(
                Key={'username': username},
                UpdateExpression="set timetableURL = :t",
                ExpressionAttributeValues={':t': data['timetableURL']},
                ReturnValues="UPDATED_NEW"
            )

            authToken = fnc.GenerateAuthToken()
            authRes = fnc.UpdateAuthToken(username, authToken)

            return fnc.SuccessResponse({'authToken': authToken}) if res['ResponseMetadata']['HTTPStatusCode'] == 200 else fnc.ErrorResponse(err.TIMETABLE_UPDATE)

        else:
            return fnc.ErrorResponse(err.INVALID_USERNAME)
    except:
        return fnc.ErrorResponse(err.UNKNOWN)
