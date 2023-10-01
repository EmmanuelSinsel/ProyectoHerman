# CONEXION SQL
from SQLConnection import SQLConnector

con = SQLConnector(host="localhost", db="biblioteca", port="3306", user="root", password="piedras123.")
con.connect()

# PROCESADOR DE JSONS
from JSONconverter import JSONtoLIST

converter = JSONtoLIST()

# MODELOS
import models

# API
# pip install fastapi
# pip install uvicorn
from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
from typing import Annotated

app = FastAPI()

# PAGINAS
import pages.Admin as Admin              # TODAS IMPLEMENTADAS, TODAS CON FUNCION, TODAS PROBADAS
import pages.Alumn as Alumn              # TODAS IMPLEMENTADAS, TODAS CON FUNCION, NINGUNA PROBADA
import pages.Author as Author            # TODAS IMPLEMENTADAS, TODAS CON FUNCION, NINGUNA PROBADA
import pages.Book as Book                # TODAS IMPLEMENTADAS, TODAS CON FUNCION, NINGUNA PROBADA
import pages.Category as Category        # TODAS IMPLEMENTADAS, TODAS CON FUNCION, NINGUNA PROBADA
import pages.Favorite as Favorite        # TODAS IMPLEMENTADAS, TODAS CON FUNCION, NINGUNA PROBADA
import pages.Library as Library          # TODAS IMPLEMENTADAS, TODAS CON FUNCION, NINGUNA PROBADA
import pages.Reserve as Reserve          # TODAS IMPLEMENTADAS, TODAS CON FUNCION, NINGUNA PROBADA
import pages.Transaction as Transaction  # TODAS IMPLEMENTADAS, TODAS CON FUNCION, NINGUNA PROBADA
import pages.Auth as Auth                # TODAS IMPLEMENTADAS, TODAS CON FUNCION, TODAS PROBADAS

# TRIGGER DE AUTENTICACION----------------------------------------------------------------------------------------------
@app.middleware("http")
async def Middleware(request: Request, call_next):
    base = str(request.base_url)
    url = str(request.url)
    if base in url:
        url = url.replace(base, '')

    if url == "docs" or url == "openapi.json":
        response = await call_next(request)
        return response
    elif url == "login":
        response = await call_next(request)
        return response
    else:
        headers = dict(request.scope['headers'])
        try:
            token = bytes.decode(headers[b'token'])
            if url == "login":
                response = await call_next(request)
                return response
            elif token == "":
                print("Not logged")
                response = {"status": "600", "msg": "Not logged"}
                return JSONResponse(content=response)
            elif (Auth.Authenticate(token)):
                print("Authenticated: " + token)
                response = await call_next(request)
                return response
            else:
                print("Invalid token")
                response = {"status": "500", "msg": "Invalid token"}
                return JSONResponse(content=response)
        except:
            return response





# AUTENTICACION---------------------------------------------------------------------------------------------------------

@app.post("/login")
async def login(request: models.Login):
    return await Auth.login(request)

@app.post("/logout")
async def logout(request: Request):
    return await Auth.logout(request)

# ADMINS----------------------------------------------------------------------------------------------------------------
@app.post("/insert_admin")
async def insert_admin(request: models.Admin):
    return Admin.insert_admin(request)

@app.post("/update_admin")
async def update_admin(request: models.Admin):
    return Admin.update_admin(request)


@app.post("/delete_admin")
async def delete_admin(request: models.Where):
    return Admin.delete_admin(request)


@app.post("/list_admin")
async def list_admin(request: models.Where):
    return await Admin.list_admin(request)


# ALUMNOS---------------------------------------------------------------------------------------------------------------
@app.post("/insert_alumn")
async def insert_alumn(request: models.Alumn):
    return await Alumn.insert_alumn(request)


@app.post("/update_alumn")
async def update_alumn(request: models.Alumn):
    return await Alumn.update_alumn(request)


@app.post("/delete_alumn")
async def delete_alumn(request: Request):
    return await Alumn.delete_alumn(request)


@app.post("/list_alumn")
async def list_alumn(request: Request):
    return await Alumn.list_alumn(request)


@app.post("/advice_alumn")
async def advice_alumn(request: models.Advice):
    return await Alumn.advice_alumn(request)


@app.post("/historial_alumn")
async def historial_alumn(request: Request):
    return await Alumn.historial_alumn(request)


@app.post("/profile_alumn")
async def profile_alumn(request: Request):
    return await Alumn.profile_alumn(request)


# LIBROS----------------------------------------------------------------------------------------------------------------
@app.post("/insert_book")
async def insert_book(request: models.Book):
    return await Book.insert_book(request)


@app.post("/update_book")
async def update_book(request: models.Book):
    return await Book.update_book(request)


@app.post("/delete_book")
async def delete_book(request: models.Where):
    return await Book.delete_book(request)


@app.post("/list_book")
async def list_book(request: models.Where):
    return await Book.list_book(request)


@app.post("/comment_book")
async def comment_book(request: models.Commentary):
    return await Book.comment_book(request)


# AUTORES---------------------------------------------------------------------------------------------------------------
@app.post("/insert_author")
async def insert_author(request: Request):
    return await Author.insert_author(request)


@app.post("/update_author")
async def update_author(request: Request):
    return await Author.update_author(request)


@app.post("/delete_author")
async def delete_author(request: Request):
    return await Author.delete_author(request)


@app.post("/list_author")
async def list_author(request: Request):
    return await Author.list_author(request)


# CATEGORIAS------------------------------------------------------------------------------------------------------------
@app.post("/insert_category")
async def insert_category(request: Request):
    return await Category.insert_category(request)


@app.post("/update_category")
async def update_category(request: Request):
    return await Category.update_category(request)


@app.post("/delete_category")
async def delete_category(request: Request):
    return await Category.delete_category(request)


@app.post("/list_category")
async def list_category(request: Request):
    return await Category.list_category(request)


# FAVORITOS-------------------------------------------------------------------------------------------------------------
@app.post("/add_favorite")
async def add_favorite(request: Request):
    return await Favorite.add_favorite(request)


# BIBLIOTECAS-----------------------------------------------------------------------------------------------------------
@app.post("/insert_library")
async def insert_library(request: Request):
    return await Library.insert_library(request)


@app.post("/update_library")
async def update_library(request: Request):
    return await Library.update_library(request)


@app.post("/delete_library")
async def delete_library(request: Request):
    return await Library.delete_library(request)


@app.post("/list_library")
async def list_library(request: Request):
    return await Library.list_library(request)


# PRESTAMOS-------------------------------------------------------------------------------------------------------------
@app.post("/insert_rental")
async def insert_rental(request: Request):
    return await Transaction.insert_rental(request)


@app.post("/update_rental")
async def update_rental(request: Request):
    return await Transaction.update_rental(request)


@app.post("/delete_rental")
async def delete_rental(request: Request):
    return await Transaction.delete_rental(request)


@app.post("/list_rental")
async def list_rental(request: Request):
    return await Transaction.list_rental(request)


# APARTADOS-------------------------------------------------------------------------------------------------------------
@app.post("/insert_reserve")
async def insert_reserve(request: Request):
    return await Reserve.insert_reserve(request)


@app.post("/update_reserve")
async def update_reserve(request: Request):
    return await Reserve.update_reserve(request)


@app.post("/delete_reserve")
async def delete_reserve(request: Request):
    return await Reserve.delete_reserve(request)


@app.post("/list_reserve")
async def list_reserve(request: Request):
    return await Reserve.list_reserve(request)


# RECOMENDACIONES-------------------------------------------------------------------------------------------------------
@app.post("/get_recomendations")
async def get_recomendations(request: Request):
    return request


# ESTADISTICAS----------------------------------------------------------------------------------------------------------
@app.post("/get_statistics")
async def get_statistics(request: Request):
    return request


# AUTOMATIZADOS---------------------------------------------------------------------------------------------------------
@app.post("/daily_deadline_check")
async def daily_deadline_check(request: Request):
    return request
