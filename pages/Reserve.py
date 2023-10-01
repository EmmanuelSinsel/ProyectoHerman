from main import con, converter
import models

table = "RESERVES"
#APARTADOS
async def insert_reserve(request: models.Reserve):
    fields, values = converter.insert(request)
    status, msg = con.insert(table=table,
                             fields=fields,
                             values=values)
    return {"message": msg, "status": status}

async def update_reserve(request: models.Reserve):
    res = request.dict()
    values = converter.update(request)
    status, msg = con.update(table=table,
                             values=values,
                             where="id_reserve = '" + res['where'] + "'")
    return {"message": msg, "status": status}

async def delete_reserve(request: models.Where):
    res = request.dict()
    status, msg = con.update(table=table,
                             values=["state = 0"],
                             where=res['where'])
    return {"message": msg, "status": status}

async def list_reserve(request: models.Where):
    res = request.dict()
    status, res = con.select(table=table,
                             where=res['where'])
    return res