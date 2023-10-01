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

def update_admin(request: models.Admin):
    res = request.dict()
    values = converter.update(request)
    status, msg = con.update(table=table,
                             values=values,
                             where="email='"+res['where']+"'")
    return {"message": msg,"status":status}

async def delete_admin(request: models.Where):
    res = request.dict()
    status, msg = con.update(table=table,
                             values=["state = 0"],
                             where=res['where'])
    return {"message": msg,"status":status}

async def list_admin(request: models.Where):
    res = request.dict()
    status, res = con.select(table=table,
                             where=res['where'])
    return res
