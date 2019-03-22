from datetime import datetime
import time
import re
from urllib import request
from bs4 import BeautifulSoup
import helpers.functions as fnc
import helpers.errors as err

def ParseTimetable(url):
    startTime = datetime.strptime("09:00", "%H:%M")
    daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    try:
        req = request.Request(url)
        opener = request.build_opener()
        response = opener.open(req)
    except:
        return fnc.ErrorResponse(err.TIMETABLE_ACCESS)

    soup = BeautifulSoup(response, "html.parser")
    dayTables = soup.findAll('table', { 'width': None })

    daysModules = []
    for i in range(len(dayTables)):
        day = dayTables[i]
        modules = day.findAll('tr')

        if len(modules):
            modules.pop(0) # Remove header titles
        else:
            modules = None

        daysModules.append({ 'day': daysOfWeek[i], 'modules': modules})

    for i in range(len(daysModules)):
        day = daysModules[i]
        modules = []
        if not day['modules']:
            continue

        for mod in day['modules']:
            parts = mod.findAll('td')

            moduleInfo = {
                'activity': parts[0].text.strip(),
                'module': {},
                'type': parts[2].text.strip(),
                'times': {
                    'start': str(datetime.strptime(parts[3].text.strip(), "%H:%M").time()),
                    'end': str(datetime.strptime(parts[4].text.strip(), "%H:%M").time())
                },
                'duration': parts[5].text.strip(),
                'weeks': [],
                'rooms': [],
                'lecturers': parts[8].text.strip().split(';'),
                'groups': []
            }

                # Module Info
            modInfo = parts[1].text.split('-')
            modCode = modInfo[0].strip()

            if len(modInfo) >= 2:
                moduleInfo['module']['code'] = CheckModuleCode(modCode)
                moduleInfo['module']['name'] = modInfo[1].strip() if len(modInfo) == 2 else '-'.join(modInfo[-2:])
            else:
                moduleInfo['module']['code'] = None
                moduleInfo['module']['name'] = modCode

                # Weeks
            weeksInfo = parts[6].text.split(',')

            for wi in weeksInfo:
                wi = wi.strip()

                if RangeOfWeeks(wi):
                    startAndEnd = wi.split('-')
                    moduleInfo['weeks'].append({ 'start': startAndEnd[0], 'end': startAndEnd[1] })
                elif SolidWeek(wi):
                    moduleInfo['weeks'].append({ 'lone': wi })

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

                    moduleInfo['rooms'].append(roomInfo)

            if len(parts[9].text.strip()):
                groups = parts[9].text.strip().split(';')
                for j in range(len(groups)):
                    groupsInfo = groups[j].split('/')
                    if len(groupsInfo) == 5:
                        groups[j] = {
                            'code': CheckCourseCode(groupsInfo[0].strip()),
                            'year': CheckCourseYear(groupsInfo[2].strip())
                        }

                moduleInfo['groups'] = groups

            modules.append(moduleInfo)
        daysModules[i]['modules'] = modules

    return { 'days': daysModules }

def CheckModuleCode(modCode):
    return modCode if re.match(r'[A-Z]{4}\d{5}', modCode) else None

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
