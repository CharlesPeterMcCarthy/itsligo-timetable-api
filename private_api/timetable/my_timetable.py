import json
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err
import public_api.timetable.modules as cl
import public_api.timetable.breaks as br

def Handler(event, context):
    data = json.loads(event['body'])
    if not fnc.ContainsAllData(data, ('studentID', 'authToken', 'timetableURL')): return fnc.ErrorResponse(err.MISSING_DETAILS)
    auth = fnc.AuthUser(data)
    if 'authOk' not in auth or not auth['authOk']: return fnc.ErrorResponse(auth)
    return GetMyTimetable(data)

def GetMyTimetable(data):
    timetable = cl.ParseTimetable(data['timetableURL'])
    hiddenModules = GetMyHiddenModules(data['studentID'], data['timetableURL'])
    if hiddenModules: timetable = RemoveHiddenModules(timetable, hiddenModules)
    timetable['days'] = br.FindBreaks(timetable['days'])
    timetable['days'] = CheckConflicts(timetable['days'])
    return fnc.SuccessResponse({'timetable': timetable, 'hiddenModules': hiddenModules})

def GetMyHiddenModules(studentID, timetableURL):
    try:
        hiddenModulesTable = fnc.GetDataTable(tbl.HIDDEN_MODS)
        res = hiddenModulesTable.get_item(Key={'studentID': studentID})
    except:
        return fnc.ErrorResponse(err.DB_QU)

    if not 'Item' in res: return None
    timetables = res['Item']['timetables']

    try:
        matchingTimetable = next(filter(lambda t: t[1]['url'] == timetableURL, enumerate(timetables)))
    except StopIteration:
        return None

    return matchingTimetable[1]['modules']

def RemoveHiddenModules(timetable, hiddenModules):
    try:
        for module in hiddenModules:
            day = next(filter(lambda t: t[1]['day'] == module['day'], enumerate(timetable['days'])))
            if day:
                matchingModule = next(filter(lambda m: (m[1]['module']['name'] == module['name'] and m[1]['times']['start'] == module['times']['start'] and m[1]['times']['end'] == module['times']['end']), enumerate(day[1]['modules'])))
                del day[1]['modules'][matchingModule[0]]
    except StopIteration:
        return timetable

    return timetable

def CheckConflicts(days):
    for day in days:
        modules = day['modules']
        if not modules: continue
        for i in range(len(modules)):
            curModuleTimes = modules[i]['times']
            nextModuleTimes = modules[i + 1]['times'] if i + 1 < len(modules) else None
            if nextModuleTimes:
                if curModuleTimes['start'] == nextModuleTimes['start'] or curModuleTimes['end'] == nextModuleTimes['end'] or (curModuleTimes['start'] < nextModuleTimes['start'] and curModuleTimes['end'] > nextModuleTimes['start']):
                    modules[i]['conflicting'] = True
                    modules[i + 1]['conflicting'] = True
    return days
