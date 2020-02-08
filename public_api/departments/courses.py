import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def Handler(event, context):
    dept = event['queryStringParameters']['department']
    return GetDepartmentCourses(dept)

def GetDepartmentCourses(dept):
    try:
        deptTable = fnc.GetDataTable(tbl.DEPTS)
        res = deptTable.get_item(
            Key={'DepartmentName': dept},
            ProjectionExpression="Courses"
        )
    except:
        return fnc.ErrorResponse(err.UNKNOWN)

    if 'Item' in res and 'Courses' in res['Item']:
        courses = res['Item']['Courses']
        for course in courses:
            del course['updatedAt']

    return fnc.SuccessResponse({ 'courses': courses })
