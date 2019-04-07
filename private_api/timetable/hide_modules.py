import json
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def Handler(event, context):
    data = json.loads(event['body'])
    if not fnc.ContainsAllData(data, ('username', 'authToken', 'timetableURL', 'modules')): return fnc.ErrorResponse(err.MISSING_DETAILS)
    auth = fnc.AuthUser(data)
    if 'authOk' not in auth or not auth['authOk']: return fnc.ErrorResponse(auth)
    return HideModule(data)

def HideModule(data):
    username = data['username']
    timetableURL = data['timetableURL']
    modules = data['modules']

    CheckForEmptyModuleNames(modules)

    try:
        hiddenModulesTable = fnc.GetDataTable(tbl.HIDDEN_MODS)
        res = hiddenModulesTable.get_item(Key={'username': username})
    except:
        return fnc.ErrorResponse(err.DB_QU)

    try:
        if 'Item' in res:
            timetables = res['Item']['timetables']
            try:
                matching = None
                matching = next(filter(lambda t: t[1]['url'] == timetableURL, enumerate(timetables)))
                if matching: res = SaveModule(hiddenModulesTable, username, matching[0], modules)
            except StopIteration:
                res = SaveTimetable(hiddenModulesTable, username, timetableURL, modules)
        else:
            res = SaveUser(hiddenModulesTable, username, timetableURL, modules)
    except:
        return fnc.ErrorResponse(err.DB_IN)

    authToken = fnc.GenerateAuthToken()
    authRes = fnc.UpdateAuthToken(username, authToken)

    return fnc.SuccessResponse({'authToken': authToken})

def CheckForEmptyModuleNames(modules):
    for module in modules:
        if module['name'] == '': module['name'] = ' '

def SaveUser(table, username, timetableURL, modules):
    return table.put_item(Item={
        'username': username,
        'timetables': [{
            'url': timetableURL,
            'modules': modules
        }]
    })

def SaveTimetable(table, username, timetableURL, modules):
    return table.update_item(
        Key={ 'username': username },
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

def SaveModule(table, username, timetableIndex, modules):
    return table.update_item(
        Key={ 'username': username },
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
