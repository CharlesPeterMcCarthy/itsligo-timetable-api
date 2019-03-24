import json
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def Handler(event, context):
    data = json.loads(event['body'])
    if not fnc.ContainsAllData(data, ('studentID', 'authToken', 'timetableURL')): return fnc.ErrorResponse(err.MISSING_DETAILS)
    auth = fnc.AuthUser(data)
    if 'authOk' not in auth or not auth['authOk']: return fnc.ErrorResponse(auth)
    return RestoreModules(data)

def RestoreModules(data):
    try:
        hiddenModulesTable = fnc.GetDataTable(tbl.HIDDEN_MODS)
        res = hiddenModulesTable.get_item(Key={'studentID': data['studentID']})
    except:
        return fnc.ErrorResponse(err.DB_QU)

    timetables = res['Item']['timetables']
    try:
        matching = None
        matching = next(filter(lambda t: t[1]['url'] == data['timetableURL'], enumerate(timetables)))
        if matching:
            res = UpdateRecord(hiddenModulesTable, data['studentID'], matching[0])
    except StopIteration:
        return fnc.ErrorResponse(err.UNKNOWN)

    return fnc.SuccessResponse(res)

def UpdateRecord(table, studentID, index):
    return table.update_item(
        Key={ 'studentID': studentID },
        UpdateExpression="REMOVE #tim[" + str(index) + "]",
        ExpressionAttributeNames={
            '#tim': 'timetables'
        },
        ReturnValues="NONE"
    )
