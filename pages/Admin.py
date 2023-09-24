from main import con, converter
from helpers import repeated
import models

#ADMINS
def insert_admin(request: models.Admin):
    res = request.dict()
    if(repeated("ADMIN","email", res['email'])==1):
        fields, values = converter.insert(request)
        status, msg = con.insert(table="ADMIN",
                                fields=fields,
                                 values=values)
        return {"message": msg,"status":status}
    else:
        return {"message": "Email already registered","status":2}

def update_admin(request: models.Admin):
    res = request.dict()
    values = converter.update(request)
    status, msg = con.update(table="ADMIN",
                             values=values,
                             where="email='"+res['email']+"'")
    return {"message": msg,"status":status}

async def delete_admin(request):
    res = await request.json()
    status, msg = con.update(table="ADMIN",
                             values=["state = 0"],
                             where="email='"+res['email']+"'")
    return {"message": msg,"status":status}

async def list_admin(request):
    res = await request.json()
    status, res = con.select(table="ADMIN",
                             where=res['where'])
    return res
