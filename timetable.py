#!flask/bin/python
from flask import Flask, jsonify, request
import urllib
import datetime
import re
from bs4 import BeautifulSoup

app = Flask(__name__)

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

def GetTimetable():
    startTime = datetime.datetime.strptime("09:00", "%H:%M")
    daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    link = "http://timetables.itsligo.ie:81/reporting/textspreadsheet;student+set;id;SG_KCOMP_H08%2FF%2FY2%2F1%2F%28A%29%0D%0A?t=student+set+textspreadsheet&days=1-7&weeks=3-9;11-16&periods=3-20&template=student+set+textspreadsheet"
    request = urllib.request.Request(link)
    opener = urllib.request.build_opener()
    response = opener.open(request)

    soup = BeautifulSoup(response, "lxml")
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

    #for cl in daysClasses[0]['classes']:
    cl = daysClasses[0]['classes'][0]
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
        'room': {},
        'lecturers': parts[8].text.strip().split(';'),
        'groups': []
    }

        # Module Info
    moduleInfo = parts[1].text.split('-')

    moduleCode = moduleInfo[0].strip()
    classInfo['module']['code'] = CheckModuleCode(moduleCode)
    moduleInfo.pop(0)

    classInfo['module']['name'] = moduleInfo[0].strip() if len(moduleInfo) == 1 else '-'.join(moduleInfo)

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
        roomInfo = parts[7].text.strip()
        roomCode = roomInfo[0:5]
        classInfo['room']['code'] = CheckRoomCode(roomCode)

        seats = re.findall(r'\([0-9]*\)', roomInfo)
        seats = seats[0].strip() if len(seats) == 1 else None
        if (seats):
            seats = seats.replace('(', '').replace(')', '')

        classInfo['room']['seats'] = CheckRoomSeats(seats)

        roomType = re.split(r'\([0-9]*\)|[A-Z]\d{4} -', roomInfo)[1].strip()
        classInfo['room']['type'] = roomType

    if len(parts[9].text.strip()):
        groups = parts[9].text.strip().split(';')
        for i in range(len(groups)):
            groupsInfo = groups[i].split('/')
            if len(groupsInfo) == 5:
                groups[i] = {
                    'code': CheckCourseCode(groupsInfo[0].strip()),
                    'year': CheckCourseYear(groupsInfo[2].strip())
                }

        classInfo['groups'] = groups

    return classInfo

@app.route('/', methods=['POST'])
def get_timetable():
    return jsonify(GetTimetable())

if __name__ == '__main__':
    app.run(debug=True)
