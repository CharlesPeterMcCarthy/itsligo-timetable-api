import json
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def Handler(event, context):
    data = json.loads(event['body'])
    if not fnc.ContainsAllData(data, ('studentID', 'authToken', 'timetableURL', 'module')): return fnc.ErrorResponse(err.MISSING_DETAILS)
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
                if matching: res = SaveModule(hiddenModulesTable, data['studentID'], matching[0], data['module'])
            except StopIteration:
                res = SaveTimetable(hiddenModulesTable, data['studentID'], data['timetableURL'], data['module'])
        else:
            res = SaveUser(hiddenModulesTable, data['studentID'], data['timetableURL'], data['module'])
    except:
        return fnc.ErrorResponse(err.DB)

    return fnc.SuccessResponse(res)

def SaveUser(table, studentID, timetableURL, module):
    return table.put_item(Item={
        'studentID': studentID,
        'timetables': [{
            'url': timetableURL,
            'modules': [ module ]
        }]
    })

def SaveTimetable(table, studentID, timetableURL, module):
    return table.update_item(
        Key={ 'studentID': studentID },
        UpdateExpression="set #tim = list_append(#tim, :tim)",
        ExpressionAttributeNames={
            '#tim': 'timetables'
        },
        ExpressionAttributeValues={
            ':tim': [{
                'url': timetableURL,
                'modules': [ module ]
            }]
         },
        ReturnValues="NONE"
    )

def SaveModule(table, studentID, timetableIndex, module):
    return table.update_item(
        Key={ 'studentID': studentID },
        UpdateExpression="set #tim[" + str(timetableIndex) + "].#mod = list_append(#tim[" + str(timetableIndex) + "].#mod, :mod)",
        ExpressionAttributeNames={
            '#tim': 'timetables',
            '#mod': 'modules'
        },
        ExpressionAttributeValues={
            ':mod': [ module ]
         },
        ReturnValues="UPDATED_NEW"
    )
