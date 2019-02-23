import json
import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def Handler(event, context):
    return GetAllDepartments()

def GetAllDepartments():
    try:
        deptTable = fnc.GetDataTable(tbl.DEPTS)
        res = deptTable.scan(
            ProjectionExpression="DepartmentName"
        )
    except:
        return fnc.ErrorResponse(err.UNKNOWN)

    if 'Items' in res:
        depts = res['Items']
        deptNames = map(lambda d: d['DepartmentName'], depts)

    return fnc.SuccessResponse({ 'departments': list(deptNames) })
