from main import con, converter
from helpers import repeated
import models


class CRUD:

    table = ""

    def __init__(self, table):
        self.table = table


    def insertNotRepeated(self, request, repeatedField):
        res = request.dict()
        if (repeated(self.table, repeatedField, res[repeatedField]) == 1):
            fields, values = converter.insert(request)
            status, msg = con.insert(table=self.table,
                                     fields=fields,
                                     values=values)
            return {"message": msg, "status": status}
        else:
            return {"message": "Email already registered", "status": 2}

    def insert(self, request):
        fields, values = converter.insert(request)
        status, msg = con.insert(table=self.table,
                                 fields=fields,
                                 values=values)
        return {"message": msg, "status": status}

    def update(self, request, updateValue):
        values = converter.update(request)
        status, msg = con.update(table=self.table,
                                 values=values,
                                 where=updateValue)
        return {"message": msg, "status": status}

    def delete(self, where: str):
        status, msg = con.update(table=self.table,
                                 values=["state = 0"],
                                 where=where)
        return {"message": msg, "status": status}

    async def list(self, where: str):
        status, res = con.select(table=self.table,
                                 where=where)
        return res
