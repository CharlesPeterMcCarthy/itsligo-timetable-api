import json
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def Handler(event, context):
    data = json.loads(event['body'])
    if not fnc.ContainsAllData(data, ('authToken', 'studentID', 'timetableURL')): return fnc.ErrorResponse(err.MISSING_DETAILS)
    auth = fnc.AuthUser(data)
    if 'authOk' not in auth or not auth['authOk']: return fnc.ErrorResponse(auth)
    return ChangeTimetable(data)

def ChangeTimetable(data):
    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.get_item(Key={'studentID': data['StudentID']})

        if 'Item' in res:
            res = userTable.update_item(
                Key={'studentID': data['studentID']},
                UpdateExpression="set timetableURL = :t",
                ExpressionAttributeValues={':t': data['timetableURL']},
                ReturnValues="UPDATED_NEW"
            )
            return fnc.SuccessResponse(res) if res['ResponseMetadata']['HTTPStatusCode'] == 200 else fnc.ErrorResponse(err.TIMETABLE_UPDATE)

        else:
            return fnc.ErrorResponse(err.INVALID_STUDENTID)
    except:
        return fnc.ErrorResponse(err.UNKNOWN)
