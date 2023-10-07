from main import con, converter
from helpers import repeated
import models
from fastapi import APIRouter, Request
from typing import Any

class CRUD:
    router = APIRouter()
    apiName = ""
    table = ""
    repeatedField = ""
    def __init__(self, Table, ApiName, RepeatedField, Model):
        self.table = Table
        self.apiName = ApiName
        self.repeatedField = RepeatedField
        model = Model
        router = self.router

        @router.post("/insertNotRepeated_"+str(self.apiName)+"/")
        async def insertNotRepeated(request: Request):
            res = await request.json()
            if (repeated(self.table, self.repeatedField, res[self.repeatedField]) == 1):
                fields, values = converter.insert(res)
                print(fields, values)
                status, msg = con.insert(table=Table,
                                         fields=fields,
                                         values=values)
                return {"message": msg, "status": status}
            else:
                return {"message": "Email already registered", "status": 2}

        @router.post("/insert_" + str(self.apiName) + "/")
        async def insert(request: Request):
            res = await request.json()
            fields, values = converter.insert(res)
            status, msg = con.insert(table=self.table,
                                     fields=fields,
                                     values=values)
            return {"message": msg, "status": status}
        @router.put("/update_" + str(self.apiName) + "/{updateValue}")
        async def update(request: Request, updateValue: str):
            res = await request.json()
            values = converter.update(res)
            status, msg = con.update(table=self.table,
                                     values=values,
                                     where=updateValue)
            return {"message": msg, "status": status}
        @router.delete("/delete_" + str(self.apiName) + "/{where}")
        def delete(where: str):
            status, msg = con.update(table=self.table,
                                     values=["state = 0"],
                                     where=where)
            return {"message": msg, "status": status}
        @router.get("/list_" + str(self.apiName) + "/{where}")
        async def list(where: str):
            status, res = con.select(table=self.table,
                                     where=where)
            return res

        @router.get("/list_" + str(self.apiName) + "/")
        async def list():
            status, res = con.select(table=self.table,
                                     where="")
            return res
