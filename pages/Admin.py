from main import con, converter
from helpers import repeated
import models

table = "ADMIN"


#ADMINS
def insert_admin(request: models.Admin):
    res = request.dict()
    if(repeated(table,"email", res['email'])==1):
        fields, values = converter.insert(request)
        status, msg = con.insert(table=table,
                                fields=fields,
                                 values=values)
        return {"message": msg,"status":status}
    else:
        return {"message": "Email already registered","status":2}

def update_admin(email: str, request: models.Admin):
    res = request.dict()
    values = converter.update(request)
    status, msg = con.update(table=table,
                             values=values,
                             where="email='"+email+"'")
    return {"message": msg,"status":status}

def delete_admin(where: str):
    status, msg = con.update(table=table,
                             values=["state = 0"],
                             where=where)
    return {"message": msg,"status":status}

async def list_admin(where: str):
    status, res = con.select(table=table,
                             where=where)
    return res
