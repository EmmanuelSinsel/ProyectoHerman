from main import converter
from manager import con
import models
from fastapi import APIRouter


class CRUD:
    router = APIRouter()

    def __init__(self, table: str, api_name: str, enabled, model: models):

        self.router.tags = [api_name.capitalize()]
        # REGISTRAR USUARIOS
        if "insert" in enabled:
            self._insert(model, api_name, table)

        if "update" in enabled:
            self._update(model, api_name, table)

        if "delete" in enabled:
            self._delete(api_name, table)

        if "select" in enabled:
            self._select(api_name, table)

        # if "account" in Enabled:
        #     @router.post("/api/register_" + str(self.apiName))
        #     async def insertAccount(request: Model):
        #         data = await insertNotRepeated(request)
        #         status = data['status']
        #         msg = data['message']
        #         print(status, msg)
        #         if status == 1:
        #             # res = request.dict()
        #             # email = str(res['email'])
        #             # type = str(1)
        #             # status = Auth.sendEmailVerification(email,type)
        #             return {"message": msg, "status": status}
        #         else:
        #             return {"message": "Email already registered", "status": 2}


    def _insert(self, model, api_name, table):
        @self.router.post("/api/insert_" + str(api_name) + "/")
        async def insert(request: model):
            res = request.dict()
            fields, values = converter.insert(res)
            status, msg = con.insert(table=table,
                                     fields=fields,
                                     values=values)
            return {"message": msg, "status": status}

    def _update(self, model, api_name, table):
        @self.router.put("/api/update_" + str(api_name) + "/{updateValue}")
        async def update(request: model, updateValue: str):
            res = request.dict()
            values = converter.update(res)
            status, msg = con.update(table=table,
                                     values=values,
                                     where=updateValue)
            return {"message": msg, "status": status}

    def _delete(self, api_name, table):
        @self.router.delete("/api/delete_" + str(api_name) + "/{where}")
        async def delete(where: str):
            status, msg = con.update(table=table,
                                     values=["state = 0"],
                                     where=where)
            return {"message": msg, "status": status}

    def _select(self, api_name, table):
        @self.router.get("/api/list_" + str(api_name) + "/{where}")
        async def select(where: str):
            status, res = con.select(table=table,
                                     where=where)
            return res


