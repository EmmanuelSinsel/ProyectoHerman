from main import con, converter
from helpers import repeated
import models
table = "CATEGORY"
#GENEROS
async def insert_category(request: models.Category):
    fields, values = converter.insert(request)
    status, msg = con.insert(table=table,
                             fields=fields,
                             values=values)
    return {"message": msg, "status": status}

async def update_category(request: models.Category):
    res = request.dict()
    values = converter.update(request)
    status, msg = con.update(table=table,
                             values=values,
                             where="email='" + res['where'] + "'")
    return {"message": msg, "status": status}

async def delete_category(request: models.Where):
    res = request.dict()
    status, msg = con.update(table=table,
                             values=["state = 0"],
                             where=res['where'])
    return {"message": msg, "status": status}

async def list_category(request: models. Where):
    res = request.dict()
    status, res = con.select(table=table,
                             where=res['where'])
    return res