import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def CheckIsAdmin(studentID):
    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.get_item(Key={ 'studentID': studentID })
    except: return err.DB_QU

    if 'Item' in res: res = res['Item']
    else: return err.INVALID_STUDENTID

    if 'accountType' in res and res['accountType'] == "Admin": return { 'isAdmin': True }
    return err.NOT_ADMIN
