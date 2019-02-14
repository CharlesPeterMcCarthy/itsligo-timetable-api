import json
import helpers.functions as fnc
import helpers.tables as tbl

def Handler(event, context):
    data = json.loads(event['body'])
    return ChangeTimetable(data) if all(d in data for d in ("StudentID", "TimetableURL")) else fnc.FormResponse({ 'error': 'Missing Details' })

def ChangeTimetable(data):
    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.get_item(Key={'StudentID': data['StudentID']})

        res = userTable.update_item(
            Key={'StudentID': data['StudentID']},
            UpdateExpression="set TimetableURL = :t",
            ExpressionAttributeValues={':t': data['TimetableURL']},
            ReturnValues="UPDATED_NEW"
        ) if 'Item' in res else { 'error': 'No user matches that Student ID' }
    except:
        res = { 'error': 'Unknown error' }

    return fnc.FormResponse(res)
