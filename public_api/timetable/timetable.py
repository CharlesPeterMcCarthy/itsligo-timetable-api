import datetime
import time
import re
import json
from urllib import request
from bs4 import BeautifulSoup
import helpers.functions as fnc

def Handler(event, context):
    data = json.loads(event['body'])
    return ParseTimetable(data['TimetableURL']) if 'TimetableURL' in data else fnc.ErrorResponse(err.MISSING_DETAILS)

def CheckModuleCode(moduleCode):
    return moduleCode if re.match(r'[A-Z]{4}\d{5}', moduleCode) else None

def CheckRoomCode(roomCode):
    return roomCode if re.match(r'[A-Z]\d{4}', roomCode) else None

def CheckRoomSeats(seats):
    return seats if re.match(r'\d+', seats) else None

def RangeOfWeeks(wi):
    return wi if re.match(r'\d{1,2}-\d{1,2}', wi) else None

def SolidWeek(wi):
    return wi if re.match(r'\d{1,2}', wi) else None

def CheckCourseCode(courseCode):
    return courseCode if re.match(r'SG_[A-Z]{5}_[A-Z]0\d', courseCode) else None

def CheckCourseYear(courseYear):
    return courseYear[1] if re.match(r'Y\d', courseYear) else None

def ParseTimetable(url):
    startTime = datetime.datetime.strptime("09:00", "%H:%M")
    daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    try:
        req = request.Request(url)
        opener = request.build_opener()
        response = opener.open(req)
    except:
        return fnc.ErrorResponse(err.TIMETABLE_ACCESS)

    soup = BeautifulSoup(response, "html.parser")
    dayTables = soup.findAll('table', { 'width': None })

    daysClasses = []
    for i in range(len(dayTables)):
        day = dayTables[i]
        classes = day.findAll('tr')

        if len(classes):
            classes.pop(0) # Remove header titles
        else:
            classes = None

        daysClasses.append({ 'day': daysOfWeek[i], 'classes': classes})

    for i in range(len(daysClasses)):
        day = daysClasses[i]
        classes = []
        if not day['classes']:
            continue

        for cl in day['classes']:
            parts = cl.findAll('td')

            classInfo = {
                'activity': parts[0].text.strip(),
                'module': {},
                'type': parts[2].text.strip(),
                'times': {
                    'start': parts[3].text.strip(),
                    'end': parts[4].text.strip()
                },
                'duration': parts[5].text.strip(),
                'weeks': [],
                'rooms': [],
                'lecturers': parts[8].text.strip().split(';'),
                'groups': []
            }

                # Module Info
            moduleInfo = parts[1].text.split('-')
            moduleCode = moduleInfo[0].strip()

            if len(moduleInfo) >= 2:
                classInfo['module']['code'] = CheckModuleCode(moduleCode)
                classInfo['module']['name'] = moduleInfo[1].strip() if len(moduleInfo) == 2 else '-'.join(moduleInfo[-2:])
            else:
                classInfo['module']['code'] = None
                classInfo['module']['name'] = moduleCode

                # Weeks
            weeksInfo = parts[6].text.split(',')

            for wi in weeksInfo:
                wi = wi.strip()

                if RangeOfWeeks(wi):
                    startAndEnd = wi.split('-')
                    classInfo['weeks'].append({ 'start': startAndEnd[0], 'end': startAndEnd[1] })
                elif SolidWeek(wi):
                    classInfo['weeks'].append({ 'lone': wi })

                # Room Info
            if len(parts[7].text.strip()):
                rooms = parts[7].text.split(';')
                for room in rooms:
                    roomInfo = {}

                    room = room.strip()
                    roomCode = room[0:5]
                    roomInfo['code'] = CheckRoomCode(roomCode)

                    seats = re.findall(r'\([0-9]*\)', room)
                    if seats:
                        seats = seats[0].strip() if len(seats) == 1 else None
                        if (seats):
                            seats = seats.replace('(', '').replace(')', '')

                        roomInfo['seats'] = CheckRoomSeats(seats)

                    roomInfo['type'] = re.split(r'\([0-9]*\)|[A-Z]\d{4} ?-', room)[1].strip()

                    classInfo['rooms'].append(roomInfo)

            if len(parts[9].text.strip()):
                groups = parts[9].text.strip().split(';')
                for j in range(len(groups)):
                    groupsInfo = groups[j].split('/')
                    if len(groupsInfo) == 5:
                        groups[j] = {
                            'code': CheckCourseCode(groupsInfo[0].strip()),
                            'year': CheckCourseYear(groupsInfo[2].strip())
                        }

                classInfo['groups'] = groups

            classes.append(classInfo)
        daysClasses[i]['classes'] = classes
    return fnc.SuccessResponse(daysClasses)
