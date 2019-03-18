import json
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def Handler(event, context):
    data = json.loads(event['body'])
    if not fnc.ContainsAllData(data, ('studentID', 'authToken', 'timetableURL', 'module')): return fnc.ErrorResponse(err.MISSING_DETAILS)
    auth = fnc.AuthUser(data)
    if 'AuthOk' not in auth or not auth['AuthOk']: return fnc.ErrorResponse(auth)
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
                if matching:
                    res = hiddenModulesTable.update_item(
                        Key={ 'studentID': data['studentID'] },
                        UpdateExpression="set #tim[" + str(matching[0]) + "].#mod = list_append(#tim[" + str(matching[0]) + "].#mod, :mod)",
                        ExpressionAttributeNames={
                            '#tim': 'timetables',
                            '#mod': 'modules'
                        },
                        ExpressionAttributeValues={
                            ':mod': [ data['module'] ]
                         },
                        ReturnValues="UPDATED_NEW"
                    )
            except StopIteration:
                res = hiddenModulesTable.update_item(
                    Key={ 'studentID': data['studentID'] },
                    UpdateExpression="set #tim = list_append(#tim, :tim)",
                    ExpressionAttributeNames={
                        '#tim': 'timetables'
                    },
                    ExpressionAttributeValues={
                        ':tim': [{
                            'url': data['timetableURL'],
                            'modules': [ data['module'] ]
                        }]
                     },
                    ReturnValues="UPDATED_NEW"
                )

        else:
            res = hiddenModulesTable.put_item(Item={
                'studentID': data['studentID'],
                'timetables': [{
                    'url': data['timetableURL'],
                    'modules': [ data['module'] ]
                }]
            })
    except:
        return fnc.ErrorResponse(err.UNKNOWN)
    return fnc.SuccessResponse(res)
