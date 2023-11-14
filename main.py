from helpers import get_book

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
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#  AUTOMATIZACIONES

#  PAGINAS
import FullManager as APIManager

Admin = APIManager.CRUD(table="admin",
                        api_name="admin",
                        enabled=["insert", "update", "delete", "select", "account"],
                        model=models.Admin)
app.include_router(Admin.router)

Alumn = APIManager.CRUD(table="ALUMN",
                        api_name="alumn",
                        enabled=["insert", "update", "delete", "select"],
                        model=models.Alumn)
app.include_router(Admin.router)

Advices = APIManager.CRUD(table="ADVICE",
                          api_name="advice",
                          enabled=["insert", "update", "delete", "select"],
                          model=models.Advice)
app.include_router(Admin.router)

Author = APIManager.CRUD(table="AUTHOR",
                         api_name="author",
                         enabled=["insert", "update", "delete", "select"],
                         model=models.Author)
app.include_router(Admin.router)

Book = APIManager.CRUD(table="BOOK",
                       api_name="book",
                       enabled=["insert", "update", "delete", "select"],
                       model=models.Book)
app.include_router(Admin.router)

Category = APIManager.CRUD(table="CATEGORY",
                           api_name="category",
                           enabled=["insert", "update", "delete", "select"],
                           model=models.Category)
app.include_router(Admin.router)

Favorite = APIManager.CRUD(table="FAVORITE",
                           api_name="favorite",
                           enabled=["insert", "update", "delete", "select"],
                           model=models.Favorite)
app.include_router(Admin.router)

Library = APIManager.CRUD(table="LIBRARY",
                          api_name="library",
                          enabled=["insert", "update", "delete", "select"],
                          model=models.Library)
app.include_router(Admin.router)

Reserve = APIManager.CRUD(table="RESERVES",
                          api_name="reserve",
                          enabled=["insert", "update", "delete", "select"],
                          model=models.Reserve)
app.include_router(Admin.router)

Transaction = APIManager.CRUD(table="TRANSACTIONS",
                              api_name="transaction",
                              enabled=["insert", "update", "delete", "select"],
                              model=models.Reserve)
app.include_router(Admin.router)

import pages.Auth as Auth


# TRIGGER DE AUTENTICACION----------------------------------------------------------------------------------------------
@app.middleware("http")
async def Middleware(request: Request, call_next):
    base = str(request.base_url)
    url = str(request.url)
    excluded_urls = ["api/login", "api/password_recover", "api/password_reset", "api/verify_email", "api/send_email_verification",
                     "api/password_token_verify", "api/authenticate"]
    if base in url:
        url = url.replace(base, '')
    if url == "docs" or url == "openapi.json":
        response = await call_next(request)

        return response
    elif url in excluded_urls:
        response = await call_next(request)
        return response
    else:
        headers = dict(request.scope['headers'])
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
                return response
            else:
                response = {"status": "401", "msg": "Invalid token"}
                return JSONResponse(content=response)
        except:
            return response

# AUTENTICACION---------------------------------------------------------------------------------------------------------

@app.post("/api/login", tags=["Authorization"])
async def login(request: models.Login):
    return await Auth.login(request)


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


# UTILITIES-------------------------------------------------------------------------------------------------------------
@app.post("/api/search_book",tags=["Authorization"])
async def search_book(request: models.GetBook):
    res = request.dict()
    return get_book(res['isbn'], res['title'])
