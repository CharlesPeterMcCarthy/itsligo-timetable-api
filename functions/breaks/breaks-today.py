import datetime
import json
from functions.timetable.timetable import GetFullTimetable

def Handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(GetTodaysBreaks())
    }

def GetTodaysBreaks():
    classes = GetTodaysClasses()
    breaks = []
    for i in range(len(classes)):
        curClass = classes[i]
        nextClass = classes[i + 1] if i + 1 < len(classes) else None
        if nextClass and curClass['times']['end'] != nextClass['times']['start']:
            breaks.append({'times': {'start': curClass['times']['end'], 'end': nextClass['times']['start']}})
    return breaks

def GetTodaysClasses():
    timetable = GetFullTimetable()
    today = datetime.datetime.today().weekday()
    classes = timetable[today]['classes']
    return classes if classes else []
