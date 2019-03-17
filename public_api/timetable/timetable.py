import json
import helpers.functions as fnc
import helpers.errors as err
import public_api.timetable.classes as cl
import public_api.timetable.breaks as br

def Handler(event, context):
    data = json.loads(event['body'])
    if not fnc.ContainsAllData(data, ('timetableURL', 'includeClasses', 'includeBreaks')): return fnc.ErrorResponse(err.MISSING_DETAILS)
    if not data['includeClasses'] and not data['includeBreaks']: return fnc.ErrorResponse(err.NO_TIMETABLE_RETURN_DATA)

    timetable = cl.ParseTimetable(data['timetableURL'])
    if data['includeBreaks']:
        timetable['days'] = br.FindBreaks(timetable['days'])
    if not data['includeClasses']:
        timetable['days'] = RemoveClasses(timetable['days'])

    if 'checkConflicts' in data and data['checkConflicts']:
        timetable['days'] = CheckConflicts(timetable['days'])

    return fnc.SuccessResponse({ 'timetable': timetable })

def RemoveClasses(days):
    for day in days:
        del day['classes']
    return days

def CheckConflicts(days):
    for day in days:
        classes = day['classes']
        if not classes: continue
        for i in range(len(classes)):
            curClassTimes = classes[i]['times']
            nextClassTimes = classes[i + 1]['times'] if i + 1 < len(classes) else None
            if nextClassTimes:
                if curClassTimes['start'] == nextClassTimes['start'] or curClassTimes['end'] == nextClassTimes['end'] or (curClassTimes['start'] < nextClassTimes['start'] and curClassTimes['end'] > nextClassTimes['start']):
                    classes[i]['conflicting'] = True
                    classes[i + 1]['conflicting'] = True
    return days
