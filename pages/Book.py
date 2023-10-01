from main import con, converter
from helpers import repeated
import models

table = "BOOK"


async def insert_book(request: models.Book):
    res = request.dict()
    if (repeated(table, "isbn", res['isbn']) == 1):
        fields, values = converter.insert(request)
        status, msg = con.insert(table=table,
                                 fields=fields,
                                 values=values)
        return {"message": msg, "status": status}
    else:
        return {"message": "Book already registered", "status": 2}


async def update_book(request):
    res = request.dict()
    values = converter.update(request)
    status, msg = con.update(table=table,
                             values=values,
                             where="isbn='" + res['where'] + "'")
    return {"message": msg, "status": status}


async def delete_book(request: models.Where):
    res = request.dict()
    status, msg = con.update(table=table,
                             values=["state = 0"],
                             where=res['where'])
    return {"message": msg, "status": status}


async def list_book(request: models.Where):
    res = request.dict()
    status, res = con.select(table=table,
                             where=res['where'])
    return res


async def comment_book(request: models.Commentary):
    fields, values = converter.insert(request)
    status, msg = con.insert(table="COMMENTARY",
                             fields=fields,
                             values=values)
    return {"message": msg, "status": status}