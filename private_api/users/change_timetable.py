import json
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def Handler(event, context):
    data = json.loads(event['body'])
    return ChangeTimetable(data) if all(d in data for d in ('StudentID', 'TimetableURL')) else fnc.ErrorResponse(err.MISSING_DETAILS)

def ChangeTimetable(data):
    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.get_item(Key={'StudentID': data['StudentID']})

        if 'Item' in res:
            res = userTable.update_item(
                Key={'StudentID': data['StudentID']},
                UpdateExpression="set TimetableURL = :t",
                ExpressionAttributeValues={':t': data['TimetableURL']},
                ReturnValues="UPDATED_NEW"
            )
            return fnc.SuccessResponse(res) if res['ResponseMetadata']['HTTPStatusCode'] == 200 else fnc.ErrorResponse(err.TIMETABLE_UPDATE)

        else:
            return fnc.ErrorResponse(err.INVALID_STUDENTID)
    except:
        return fnc.ErrorResponse(err.UNKNOWN)
