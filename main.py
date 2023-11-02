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
from typing import Annotated

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

Admin = APIManager.CRUD(Table="admin", ApiName="admin", RepeatedField="email", Enabled="IUDLWA", Model=models.Admin)
app.include_router(Admin.router)

Alumn = APIManager.CRUD(Table="ALUMN", ApiName="alumn", RepeatedField="email", Enabled="IUDLW", Model=models.Alumn)
app.include_router(Admin.router)

Advices = APIManager.CRUD(Table="ADVICE", ApiName="advice", RepeatedField="", Enabled="RUDLW", Model=models.Advice)
app.include_router(Admin.router)

Author = APIManager.CRUD(Table="AUTHOR", ApiName="author", RepeatedField="", Enabled="RUDLW", Model=models.Author)
app.include_router(Admin.router)

Book = APIManager.CRUD(Table="BOOK", ApiName="book", RepeatedField="isbn", Enabled="IUDLW", Model=models.Book)
app.include_router(Admin.router)

Category = APIManager.CRUD(Table="CATEGORY", ApiName="category", RepeatedField="", Enabled="RUDLW",
                           Model=models.Category)
app.include_router(Admin.router)

Favorite = APIManager.CRUD(Table="FAVORITE", ApiName="favorite", RepeatedField="", Enabled="RUDLW",
                           Model=models.Favorite)
app.include_router(Admin.router)

Library = APIManager.CRUD(Table="LIBRARY", ApiName="library", RepeatedField="email", Enabled="IUDLW",
                          Model=models.Library)
app.include_router(Admin.router)

Reserve = APIManager.CRUD(Table="RESERVES", ApiName="reserve", RepeatedField="", Enabled="RUDLW", Model=models.Reserve)
app.include_router(Admin.router)

Transaction = APIManager.CRUD(Table="TRANSACTIONS", ApiName="transaction", RepeatedField="", Enabled="RUDLW",
                              Model=models.Reserve)
app.include_router(Admin.router)

import pages.Auth as Auth


# TRIGGER DE AUTENTICACION----------------------------------------------------------------------------------------------
@app.middleware("http")
async def Middleware(request: Request, call_next):
    base = str(request.base_url)
    url = str(request.url)
    excluded_urls = ["api/login", "api/password_recover", "api/password_reset", "api/verify_email", "api/send_email_verification",
                     "api/password_token_verify"]
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
            print(token)
            if url == "login":
                response = await call_next(request)
                headers = {"Access-Control-Allow-Origin": "*"}
                return JSONResponse(content=response, headers=headers)
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

@app.post("/api/login")
async def login(request: models.Login):
    return await Auth.login(request)


@app.post("/api/logout")
async def logout(request: Request):
    return await Auth.logout(request)


@app.post("/api/password_recover")
async def passwordRecover(request: Request):
    return await Auth.sendRecoverToken(request)

@app.post("/api/password_token_verify")
async def passwordTokenVerify(request: Request):
    return await Auth.VerifyPasswordToken(request)

@app.post("/api/password_reset")
async def passwordReset(request: Request):
    return await Auth.PasswordReset(request)


@app.post("/api/send_email_verification")
async def sendEmailVerification(request: Request):
    return await Auth.sendEmailVerification(request)


@app.post("/api/verify_email")
async def verifyEmail(request: Request):
    return await Auth.emailVerification(request)


# UTILITIES-------------------------------------------------------------------------------------------------------------
@app.post("/api/search_book")
async def search_book(request: models.GetBook):
    res = request.dict()
    return get_book(res['isbn'], res['title'])
