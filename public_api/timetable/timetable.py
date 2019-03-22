import json
import helpers.functions as fnc
import helpers.errors as err
import public_api.timetable.modules as mod
import public_api.timetable.breaks as br

def Handler(event, context):
    data = json.loads(event['body'])
    if not fnc.ContainsAllData(data, ('timetableURL', 'includeModules', 'includeBreaks')): return fnc.ErrorResponse(err.MISSING_DETAILS)
    if not data['includeModules'] and not data['includeBreaks']: return fnc.ErrorResponse(err.NO_TIMETABLE_RETURN_DATA)

    timetable = mod.ParseTimetable(data['timetableURL'])
    if data['includeBreaks']:
        timetable['days'] = br.FindBreaks(timetable['days'])
    if not data['includeModules']:
        timetable['days'] = RemoveModules(timetable['days'])

    if 'checkConflicts' in data and data['checkConflicts']:
        timetable['days'] = CheckConflicts(timetable['days'])

    return fnc.SuccessResponse({ 'timetable': timetable })

def RemoveModules(days):
    for day in days:
        del day['modules']
    return days

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
