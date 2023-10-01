from main import con, converter
from helpers import repeated
import models

table = "AUTHOR"
#AUTORES
async def insert_author(request: models.Author):
    fields, values = converter.insert(request)
    status, msg = con.insert(table=table,
                             fields=fields,
                             values=values)
    return {"message": msg, "status": status}


async def update_author(request: models.Author):
    res = request.dict()
    values = converter.update(request)
    status, msg = con.update(table=table,
                             values=values,
                             where="id_author ='" + res['where'] + "'")
    return {"message": msg, "status": status}

async def delete_author(request: models.Where):
    res = request.dict()
    status, msg = con.update(table=table,
                             values=["state = 0"],
                             where=res['where'])
    return {"message": msg, "status": status}

async def list_author(request: models.Where):
    res = request.dict()
    status, res = con.select(table=table,
                             where=res['where'])
    return res