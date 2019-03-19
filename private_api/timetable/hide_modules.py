import json
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def Handler(event, context):
    data = json.loads(event['body'])
    if not fnc.ContainsAllData(data, ('studentID', 'authToken', 'timetableURL', 'modules')): return fnc.ErrorResponse(err.MISSING_DETAILS)
    auth = fnc.AuthUser(data)
    if 'authOk' not in auth or not auth['authOk']: return fnc.ErrorResponse(auth)
    return HideModule(data)

def HideModule(data):
    try:
        hiddenModulesTable = fnc.GetDataTable(tbl.HIDDEN_MODS)
        res = hiddenModulesTable.get_item(Key={'studentID': data['studentID']})

        if 'Item' in res:
            timetables = res['Item']['timetables']
            try:
                matching = None
                matching = next(filter(lambda t: t[1]['url'] == data['timetableURL'], enumerate(timetables)))
                if matching: res = SaveModule(hiddenModulesTable, data['studentID'], matching[0], data['modules'])
            except StopIteration:
                res = SaveTimetable(hiddenModulesTable, data['studentID'], data['timetableURL'], data['modules'])
        else:
            res = SaveUser(hiddenModulesTable, data['studentID'], data['timetableURL'], data['modules'])
    except:
        return fnc.ErrorResponse(err.DB)

    return fnc.SuccessResponse(res)

def SaveUser(table, studentID, timetableURL, modules):
    return table.put_item(Item={
        'studentID': studentID,
        'timetables': [{
            'url': timetableURL,
            'modules': modules
        }]
    })

def SaveTimetable(table, studentID, timetableURL, modules):
    return table.update_item(
        Key={ 'studentID': studentID },
        UpdateExpression="set #tim = list_append(#tim, :tim)",
        ExpressionAttributeNames={
            '#tim': 'timetables'
        },
        ExpressionAttributeValues={
            ':tim': [{
                'url': timetableURL,
                'modules': modules
            }]
         },
        ReturnValues="NONE"
    )

def SaveModule(table, studentID, timetableIndex, modules):
    return table.update_item(
        Key={ 'studentID': studentID },
        UpdateExpression="set #tim[" + str(timetableIndex) + "].#mod = list_append(#tim[" + str(timetableIndex) + "].#mod, :mod)",
        ExpressionAttributeNames={
            '#tim': 'timetables',
            '#mod': 'modules'
        },
        ExpressionAttributeValues={
            ':mod': modules
         },
        ReturnValues="UPDATED_NEW"
    )
