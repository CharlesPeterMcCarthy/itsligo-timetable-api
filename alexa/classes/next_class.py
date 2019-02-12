import datetime
import time
import json
from public_api.timetable.timetable import GetFullTimetable

def Handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(GetNextClass())
    }

def GetNextClass():
    timetable = GetFullTimetable()
    today = datetime.datetime.today().weekday()
    curTime = datetime.datetime.now().time()
    i = today
    while i < len(timetable):
        nextClassDay = timetable[i]
        if nextClassDay['classes'] and (curTime < datetime.datetime.time(datetime.datetime.strptime(nextClassDay['classes'][len(nextClassDay['classes']) - 1]['times']['start'], '%H:%M')) or i != today):
            break
        else:
            i = i + 1 if i < 6 else 0

    for cl in nextClassDay['classes']:
        if curTime < datetime.datetime.time(datetime.datetime.strptime(cl['times']['start'], '%H:%M')) or i != today:
            nextClass = cl
            break

    nextClass = { 'class': cl, 'day': nextClassDay['day'], 'isToday': i == today }

    if nextClass['isToday']:
        nextClass['startsIn'] = GetTimeUntilClass(cl['times']['start'])

    return nextClass

def GetTimeUntilClass(time):
    curDatetime = datetime.datetime.now()
    timeParts = time.split(':')
    classDatetime = curDatetime.replace(hour = int(timeParts[0]), minute = int(timeParts[1]))
    secondsDiff = (classDatetime - curDatetime).total_seconds()
    hoursDiff = int(secondsDiff / (60 * 60))
    minutesDiff = int((secondsDiff / 60) - (hoursDiff * 60))
    return { 'hours': hoursDiff, 'minutes': minutesDiff }
