import json
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def Handler(event, context):
    data = json.loads(event['body'])
    if not fnc.ContainsAllData(data, ('username', 'authToken', 'timetableURL')): return fnc.ErrorResponse(err.MISSING_DETAILS)
    auth = fnc.AuthUser(data)
    if 'authOk' not in auth or not auth['authOk']: return fnc.ErrorResponse(auth)
    return RestoreModules(data)

def RestoreModules(data):
    username = data['username']

    try:
        hiddenModulesTable = fnc.GetDataTable(tbl.HIDDEN_MODS)
        res = hiddenModulesTable.get_item(Key={'username': username})
    except:
        return fnc.ErrorResponse(err.DB_QU)

    timetables = res['Item']['timetables']
    try:
        matching = None
        matching = next(filter(lambda t: t[1]['url'] == data['timetableURL'], enumerate(timetables)))
        if matching:
            res = UpdateRecord(hiddenModulesTable, username, matching[0])
    except StopIteration:
        return fnc.ErrorResponse(err.UNKNOWN)

    return fnc.SuccessResponse(res)

def UpdateRecord(table, username, index):
    return table.update_item(
        Key={'username': username},
        UpdateExpression="REMOVE #tim[" + str(index) + "]",
        ExpressionAttributeNames={
            '#tim': 'timetables'
        },
        ReturnValues="NONE"
    )
