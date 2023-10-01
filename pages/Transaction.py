from main import con, converter
from helpers import repeated
import models
table="TRANSACTIONS"
#PRESTAMOS
async def insert_rental(request: models.Transaction):
    fields, values = converter.insert(request)
    status, msg = con.insert(table=table,
                             fields=fields,
                             values=values)
    return {"message": msg, "status": status}

async def update_rental(request: models.Transaction):
    res = request.dict()
    values = converter.update(request)
    status, msg = con.update(table=table,
                             values=values,
                             where="id_transaction='" + res['where'] + "'")
    return {"message": msg, "status": status}

async def delete_rental(request: models.Where):
    res = request.dict()
    status, msg = con.update(table=table,
                             values=["state = 0"],
                             where=res['where'])
    return {"message": msg, "status": status}

async def list_rental(request: models.Where):
    res = request.dict()
    status, res = con.select(table=table,
                             where=res['where'])
    return res