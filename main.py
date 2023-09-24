#CONEXION SQL
from SQLConnection import SQLConnector
con = SQLConnector(host="localhost",
                     db="biblioteca",
                   port="3306",
                   user="root",
               password="piedras123.")
con.connect()

#PROCESADOR DE JSONS
from JSONconverter import JSONtoLIST
converter = JSONtoLIST()

#MODELOS
import models

#API
#pip install fastapi
#pip install uvicorn
from fastapi import FastAPI, Request
app = FastAPI()

#HELPERS

def repeated(table, field, value):
    sentence = field + "='"+value+"'"
    status, msg = con.repeated(table=table,
                               where=sentence)
    return status
#ADMINS
@app.post("/insert_admin")
def insert_admin(request: models.Admin):
    res = request.dict()
    if(repeated("ADMIN","email", res['email'])==1):
        fields, values = converter.insert(request)
        status, msg = con.insert(table="ADMIN",
                                fields=fields,
                                 values=values)
        return {"message": msg,"status":status}
    else:
        return {"message": "Email already registered","status":2}

@app.post("/update_admin")
def update_admin(request: models.Admin):
    res = request.dict()
    values = converter.update(request)
    status, msg = con.update(table="ADMIN",
                             values=values,
                             where="email='"+res['email']+"'")
    return {"message": msg,"status":status}

@app.post("/delete_admin")
async def delete_admin(request: Request):
    res = await request.json()
    print(res)
    status, msg = con.update(table="ADMIN",
                             values=["state = 0"],
                             where="email='"+res['email']+"'")
    return {"message": msg,"status":status}

@app.post("/list_admin")
async def list_admin(request: Request):
    res = await request.json()
    status, res = con.select(table="ADMIN",
                             where=res['where'])
    return res

#ALUMNOS
@app.post("/insert_alumn")
def insert_alumn(request: Request):
    return request

@app.post("/update_alumn")
def update_alumn(request: Request):
    return request

@app.post("/delete_alumn")
def delete_alumn(request: Request):
    return request

@app.post("/list_alumn")
def list_alumn(request: Request):
    return request

@app.post("/advice_alumn")
def advice_alumn(request: Request):
    return request

@app.post("/historial_alumn")
def historial_alumn(request: Request):
    return request

@app.post("/profile_alumn")
def profile_alumn(request: Request):
    return request

#LIBROS
@app.post("/insert_book")
def insert_book(request: Request):
    return request

@app.post("/update_book")
def update_book(request: Request):
    return request

@app.post("/delete_book")
def delete_book(request: Request):
    return request

@app.post("/list_book")
def list_book(request: Request):
    return request

@app.post("/comment_book")
def comment_book(request: Request):
    return request

#AUTORES
@app.post("/insert_author")
def insert_author(request: Request):
    return request

@app.post("/update_author")
def update_author(request: Request):
    return request

@app.post("/delete_author")
def delete_author(request: Request):
    return request

@app.post("/list_author")
def list_author(request: Request):
    return request

#GENEROS
@app.post("/insert_category")
def insert_category(request: Request):
    return request

@app.post("/update_category")
def update_category(request: Request):
    return request

@app.post("/delete_category")
def delete_category(request: Request):
    return request

@app.post("/list_category")
def list_category(request: Request):
    return request

#FAVORITOS
@app.post("/add_favorite")
def add_favorite(request: Request):
    return request

#PRESTAMOS
@app.post("/insert_rental")
def insert_rental(request: Request):
    return request

@app.post("/update_rental")
def update_rental(request: Request):
    return request

@app.post("/delete_rental")
def delete_rental(request: Request):
    return request

@app.post("/list_rental")
def list_rental(request: Request):
    return request

#APARTADOS
@app.post("/insert_reserve")
def insert_reserve(request: Request):
    return request

@app.post("/update_reserve")
def update_reserve(request: Request):
    return request

@app.post("/delete_reserve")
def delete_reserve(request: Request):
    return request

@app.post("/list_reserve")
def list_reserve(request: Request):
    return request

#RECOMENDACIONES
@app.post("/get_recomendations")
def get_recomendations(request: Request):
    return request

#ESTADISTICAS
@app.post("/get_statistics")
def get_statistics(request: Request):
    return request

#AUTOMATIZADOS
@app.post("/daily_deadline_check")
def daily_deadline_check(request: Request):
    return request