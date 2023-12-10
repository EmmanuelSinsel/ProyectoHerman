import helpers
from helpers import get_book, get_fields
from typing import Annotated
# PROCESADOR DE JSONS
from JSONconverter import JSONtoLIST

converter = JSONtoLIST()

# MODELOS
import models

# API
# pip install fastapi
# pip install uvicorn
from fastapi import FastAPI, Request, Header, Response
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
#  AUTOMATIZACIONES

#  PAGINAS
import FullManager as APIManager

Admin = APIManager.CRUD(table="admin",
                        api_name="admin",
                        enabled=["insert", "update", "delete", "select", "account"],
                        model=models.Admin)
app.include_router(Admin.router)

Alumn = APIManager.CRUD(table="alumn",
                        api_name="alumn",
                        enabled=["insert", "update", "delete", "select"],
                        model=models.Alumn)
app.include_router(Admin.router)

Advices = APIManager.CRUD(table="advice",
                          api_name="advice",
                          enabled=["insert", "update", "delete", "select"],
                          model=models.Advice)
app.include_router(Admin.router)

Author = APIManager.CRUD(table="author",
                         api_name="author",
                         enabled=["insert", "update", "delete", "select"],
                         model=models.Author)
app.include_router(Admin.router)

Book = APIManager.CRUD(table="book",
                       api_name="book",
                       enabled=["insert", "update", "delete", "select"],
                       model=models.Book)
app.include_router(Admin.router)

Category = APIManager.CRUD(table="category",
                           api_name="category",
                           enabled=["insert", "update", "delete", "select"],
                           model=models.Category)
app.include_router(Admin.router)

Favorite = APIManager.CRUD(table="favorite",
                           api_name="favorite",
                           enabled=["insert", "update", "delete", "select"],
                           model=models.Favorite)
app.include_router(Admin.router)

Library = APIManager.CRUD(table="library",
                          api_name="library",
                          enabled=["insert", "update", "delete", "select"],
                          model=models.Library)
app.include_router(Admin.router)

Reserve = APIManager.CRUD(table="reserves",
                          api_name="reserve",
                          enabled=["insert", "update", "delete", "select"],
                          model=models.Reserve)
app.include_router(Admin.router)

Transaction = APIManager.CRUD(table="transactions",
                              api_name="loan",
                              enabled=["insert", "update", "delete", "select"],
                              model=models.Transaction)
app.include_router(Admin.router)

Transaction = APIManager.CRUD(table="log",
                              api_name="log",
                              enabled=["select"],
                              model=models.Log)
app.include_router(Admin.router)

Token = APIManager.CRUD(table="token",
                              api_name="token",
                              enabled=["select"],
                              model=models.Token)
app.include_router(Admin.router)

import pages.Auth as Auth
import pages.Loans as Loans
import pages.Reserves as Reserves
import pages.Book as Books
import pages.Advices as Advices
import pages.Statistics as Statistics

# TRIGGER DE AUTENTICACION----------------------------------------------------------------------------------------------
@app.middleware("http")
async def Middleware(request: Request, call_next):
    headers = dict(request.scope['headers'])
    base = str(request.base_url)
    url = str(request.url)
    excluded_urls = ["api/login", "api/password_recover", "api/password_reset", "api/verify_email", "api/send_email_verification",
                     "api/password_token_verify", "api/authenticate", "api/insert_alumn/", "api/send_email_verification",
                     "api/verify_email"]
    if b'access-control-request-headers' in headers:
        response = await call_next(request)
        return response
    if base in url:
        url = url.replace(base, '')
    if url == "docs" or url == "openapi.json":
        response = await call_next(request)
        return response
    elif url in excluded_urls:
        print("hola")
        headers = {"Access-Control-Allow-Origin": "*"}
        response = await call_next(request)
        return response
    else:
        try:
            token = request.headers.get('token')
            if url == "login":
                response = await call_next(request)
                headers = {"Access-Control-Allow-Origin": "*"}
                return JSONResponse(content=response, headers=headers)
            elif token == "":
                response = {"status": "401", "msg": "Not logged"}
                return JSONResponse(content=response)
            elif (Auth.Authenticate(token)):
                response = await call_next(request)
                headers = {"Access-Control-Allow-Origin": "*"}
                return JSONResponse(content=response, headers=headers)
            else:
                response = {"status": "401", "msg": "Invalid token"}
                return JSONResponse(content=response)
        except:
            return response

# AUTENTICACION---------------------------------------------------------------------------------------------------------

@app.post("/api/login", tags=["Authorization"])
async def login(request: models.Login):
    return await Auth.login(request)

@app.post("/api/get_token_data", tags=["Authorization"])
async def get_token_data(request: Request):
    return await Auth.get_token_data(request)

@app.post("/api/logout",tags=["Authorization"])
async def logout(request: Request):
    return await Auth.logout(request)

@app.post("/api/authenticate",tags=["Authorization"])
async def logout(request: Request):
    return await Auth.authenticate_self(request)

@app.post("/api/password_recover",tags=["Authorization"])
async def passwordRecover(request: Request):
    return await Auth.sendRecoverToken(request)

@app.post("/api/password_token_verify",tags=["Authorization"])
async def passwordTokenVerify(request: Request):
    return await Auth.VerifyPasswordToken(request)

@app.post("/api/password_reset",tags=["Authorization"])
async def passwordReset(request: Request):
    return await Auth.PasswordReset(request)


@app.post("/api/send_email_verification",tags=["Authorization"])
async def sendEmailVerification(request: Request):
    return await Auth.sendEmailVerification(request)


@app.post("/api/verify_email",tags=["Authorization"])
async def verifyEmail(request: Request):
    return await Auth.emailVerification(request)


# PRESTAMOS-------------------------------------------------------------------------------------------------------------
@app.post("/api/get_full_loan", tags=["Loan"])
async def get_full_loan(request: Request):
  return await Loans.get_full_loan(request)

@app.post("/api/register_loan", tags=["Loan"])
async def register_loan(request: Request):
  return await Loans.register_loan(request)

@app.post("/api/update_loan", tags=["Loan"])
async def update_loan(request: Request):
  return await Loans.update_loan(request)

@app.post("/api/get_book_data", tags=["Book"])
async def get_book_data(request: Request):
  return await Loans.get_book_data(request)

@app.post("/api/send_return_mail", tags=["Loan"])
async def get_book_data(request: Request):
  return await Loans.send_return_mail(request)


# RESERVAS--------------------------------------------------------------------------------------------------------------

@app.post("/api/get_full_reserve", tags=["Reserve"])
async def get_full_loan(request: Request):
  return await Reserves.get_full_reserves(request)

# LIBROS----------------------------------------------------------------------------------------------------------------

@app.post("/api/get_full_book", tags=["Book"])
async def get_full_book(request: Request):
  return await Books.get_full_book(request)

@app.post("/api/register_book", tags=["Book"])
async def register_loan(request: Request):
  return await Books.register_book(request)

@app.post("/api/update_book", tags=["Loan"])
async def update_loan(request: Request):
  return await Books.update_book(request)

# OBSERVACIONES---------------------------------------------------------------------------------------------------------

@app.post("/api/get_full_advice", tags=["Advice"])
async def get_full_book(request: Request):
  return await Advices.get_full_advice(request)

@app.post("/api/register_advice", tags=["Advice"])
async def register_loan(request: Request):
  return await Advices.register_advice(request)

# UTILITIES-------------------------------------------------------------------------------------------------------------
@app.post("/api/search_book",tags=["Utilidad"])
async def search_book(request: models.GetBook):
    res = request.dict()
    return get_book(res['isbn'], res['title'])

@app.post("/api/get_model",tags=["Utilidad"])
async def get_model(request: Request):
    res = await request.json()
    return get_fields(res['table'])

@app.post("/api/log",tags=["Utilidad"])
async def log(request: Request):
    return await Auth.log(request)

#STATISTICS-------------------------------------------------------------------------------------------------------------
@app.get("/api/get_full_statistics",tags=["Estadisticas"])
async def get_full_dashboard():
    return await Statistics.get_full_dashboard()

#ADMINISTRADORES--------------------------------------------------------------------------------------------------------

@app.post("/api/get_admin_profile",tags=["Admin"])
async def get_full_dashboard(request: Request):
    return await helpers.get_admin_profile(request)

@app.post("/api/get_alumn_profile",tags=["Admin"])
async def get_full_dashboard(request: Request):
    return await helpers.get_alumn_profile(request)
