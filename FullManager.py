from main import converter
from manager import con
from helpers import repeated
import models
from fastapi import APIRouter, Request
from typing import Any
import pages.Auth as Auth

class CRUD:
    router = APIRouter()
    apiName = ""
    table = ""
    repeatedField = ""
    enabled = ""

    def __init__(self, Table: str, ApiName: str, RepeatedField: str, Enabled: str, Model: models):
        self.table = Table
        self.apiName = ApiName
        self.repeatedField = RepeatedField
        self.enabledMethods = Enabled
        router = self.router

        # I - INSERT
        # R - INSERT NOT REPEATED
        # U - UPDATE
        # D - DELETE
        # S - SELECT
        # W - SELECT WHERE
        # A - CREATE ACCOUNT
        #
        if "I" in Enabled:
            @router.post("/insertNotRepeated_" + str(self.apiName) + "/")
            async def insertNotRepeated(request: Model):
                res = request.dict()
                if (repeated(self.table, self.repeatedField, res[self.repeatedField]) == 1):
                    fields, values = converter.insert(res)
                    print(fields, values)
                    status, msg = con.insert(table=Table,
                                             fields=fields,
                                             values=values)
                    return {"message": msg, "status": status}
                else:
                    return {"message": "Email already registered", "status": 2}

        if "R" in Enabled:
            @router.post("/insert_" + str(self.apiName) + "/")
            async def insert(request: Model):
                res = request.dict()
                fields, values = converter.insert(res)
                status, msg = con.insert(table=self.table,
                                         fields=fields,
                                         values=values)
                return {"message": msg, "status": status}

        if "U" in Enabled:
            @router.put("/update_" + str(self.apiName) + "/{updateValue}")
            async def update(request: Model, updateValue: str):
                res = request.dict()
                values = converter.update(res)
                status, msg = con.update(table=self.table,
                                         values=values,
                                         where=updateValue)
                return {"message": msg, "status": status}

        if "D" in Enabled:
            @router.delete("/delete_" + str(self.apiName) + "/{where}")
            def delete(where: str):
                status, msg = con.update(table=self.table,
                                         values=["state = 0"],
                                         where=where)
                return {"message": msg, "status": status}

        if "S" in Enabled:
            @router.get("/list_" + str(self.apiName) + "/{where}")
            async def list(where: str):
                status, res = con.select(table=self.table,
                                         where=where)
                return res

        if "W" in Enabled:
            @router.get("/list_" + str(self.apiName) + "/")
            async def list():
                status, res = con.select(table=self.table,
                                         where="")
                return res

        # REGISTRAR USUARIOS

        if "A" in Enabled:
            @router.get("/register_" + str(self.apiName) + "/")
            async def insertAccount(request: Model):
                status, msg = insertNotRepeated(request)
                if status == 1:
                    res = request.dict()
                    status = Auth.sendEmail(res['email'])
                    return {"message": msg, "status": status}
                else:
                    return {"message": "Email already registered", "status": 2}

class types:
    isForeignKey: bool
    isPrimaryKey: bool
    autoIncremental: bool
