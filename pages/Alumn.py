from main import con, converter
from helpers import repeated
import models

table = "ALUMN"


def insert_alumn(request: models.Alumn):
    res = request.dict()
    if (repeated("ALUMN", "email", res['email']) == 1):
        fields, values = converter.insert(request)
        status, msg = con.insert(table=table,
                                 fields=fields,
                                 values=values)
        return {"message": msg, "status": status}
    else:
        return {"message": "Email already registered", "status": 2}


def update_alumn(request: models.Alumn):
    res = request.dict()
    values = converter.update(request)
    status, msg = con.update(table=table,
                             values=values,
                             where=res['where'])
    return {"message": msg, "status": status}


async def delete_alumn(request: models.Where):
    res = await request.json()
    status, msg = con.update(table=table,
                             values=["state = 0"],
                             where=res['where'])
    return {"message": msg, "status": status}


async def list_alumn(request: models.Where):
    res = await request.json()
    status, res = con.select(table=table,
                             where=res['where'])
    return res


def advice_alumn(request: models.Advice):
    fields, values = converter.insert(request)
    status, msg = con.insert(table="ADVICE",
                             fields=fields,
                             values=values)
    return {"message": msg, "status": status}


async def historial_alumn(request: models.Where):
    res = await request.json()
    status, res = con.select(table="TRANSACTIONS",
                             where=res['where'])
    return res


async def profile_alumn(request):
    res = await request.json()
    status, res = con.select(table=table,
                             where=res['where'])
    return res
