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

    return fnc.SuccessResponse({ 'timetable': timetable })

def RemoveClasses(days):
    for day in days:
        del day['classes']
    return days
