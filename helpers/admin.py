import helpers.functions as fnc
import helpers.tables as tbl
import helpers.errors as err

def CheckIsAdmin(username):
    try:
        userTable = fnc.GetDataTable(tbl.USERS)
        res = userTable.get_item(Key={'username': username})
    except:
        return err.DB_QU

    if 'Item' in res: res = res['Item']
    else:
        return err.INVALID_USERNAME

    if 'accountType' in res and res['accountType'] == "Admin":
        return {'isAdmin': True}
    return err.NOT_ADMIN
