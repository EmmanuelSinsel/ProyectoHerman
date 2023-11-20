import helpers
from main import converter
from manager import con
import models
from fastapi import APIRouter

class CRUD:
    router = APIRouter()
    table = ""
    def __init__(self, table: str, api_name: str, enabled, model: models):
        self.table = table
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

    def _insert(self, model, api_name, table):
        @self.router.post("/api/insert_" + str(api_name) + "/")
        async def insert(request: model):

            res = request.dict()
            print(res)
            fields, values = converter.insert(res)
            print(fields, values)
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
            fields = helpers.get_fields(self.table)
            if where == "*":
                where = ""
            status, res = con.select(table=table,
                                     where=where)
            response = {}
            res_list = list(res)
            for i in range(len(res_list)):
                data = {}
                for j in range(len(fields)):
                    data[fields[j]['Field']]=res_list[i][j]
                response[str(i)]=data
            return response


