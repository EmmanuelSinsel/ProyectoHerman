import datetime
import random
import string
from datetime import date, timedelta
from manager import con
import models
from dateutil.parser import parse
from fastapi import Request
import smtplib
from email.mime.text import MIMEText
# TOKENS
characters = string.ascii_letters + string.digits
token_expiration_time = 30  # DIAS


def generate_token(id_user, type_user):
    flag = 0
    while flag == 0:
        token = ''.join(random.choice(characters) for i in range(30))
        print("Generated Token: "+token)

        status, res = con.select(table="token",
                                 where="token = '" + token + "'")
        if len(res) == 0:
            break
    expiration_date = date.today()+ timedelta(days=token_expiration_time)
    print(id_user, type_user, token, expiration_date)
    con.insert(table="token",
               fields="id_user, type_user, token, expiration_date, expired",
               values=[str(id_user), str(type_user), str(token), str(expiration_date), "0"])
    return {"status": "1", "msg": "Sucessful login", "token": token}

async def authorize(request: Request, type: string):
    token = request.headers.get('token')
    status, res = con.select(table="token",
                             where="token = '" + token + "'")
    if (len(res) > 0):
        if res[0][5] == "0":
            expiration_date = parse(str(res[0][4]))
            today = parse(str(date.today()))
            if expiration_date > today:
                if res[0][2] == type:
                    return True
            else:
                con.update(table="token",
                           values=["expired = '1'"],
                           where="id_token = " + str(res[0][0]))
                return False
        if res[0][5] == "1":
            return False
def Authenticate(token):

    status, res = con.select(table="token",
                             where="token = '" + token + "'")
    if(len(res)>0):
        if res[0][5] == "0":
            expiration_date = parse(str(res[0][4]))
            today = parse(str(date.today()))
            if expiration_date > today:
                print("Authentication Succesful")
                return True
            else:
                con.update(table="token",
                           values=["expired = '1'"],
                           where="id_token = "+str(res[0][0]))
                print("Authentication Failed")
                return False
        if res[0][5] == "1":
            print("Authentication Failed")
            return False

async def authenticate_self(request: Request):
    resource = await request.json()
    token = resource['token']
    status, res = con.select(table="token",
                             where="token = '" + token + "'")
    if(len(res)>0):
        if res[0][5] == "0":
            expiration_date = parse(str(res[0][4]))
            today = parse(str(date.today()))
            if expiration_date > today:
                print("Authentication Succesful")
                return {"status": "1", "msg": "Succesful Auth"}
            else:
                con.update(table="token",
                           values=["expired = '1'"],
                           where="id_token = "+res[0][0])
                print("Authentication Failed")
                return {"status": "0", "msg": "Expired Token"}
        if res[0][5] == "1":
            return {"status": "0", "msg": "Expired Token"}

# AUTHENTICATION
async def login(request: models.Login):
    resource = request.dict()
    print(resource)
    if not resource['token'] == "":
        if Authenticate(resource['token']):
            return {"status": "400", "msg": "Valid token", "token": "", "type": resource['type']}
        else:
            return {"status": "500", "msg": "Invalid token", "token": "", "type": resource['type']}
    user_type = resource["type"]
    email = resource["email"]
    if user_type == "1" and not email == "":  # LOGIN ADMIN
        status, res = con.select(table="admin",
                                 where="email = '"+email+"'")
        print(res)
        if(len(res)>=1):
            if res[0][2] == resource['password']:
                return generate_token(res[0][0], user_type)
            else:
                return {"status": "0", "msg": "Wrong password", "token": ""}
        else:
            return {"status": "2", "msg": "Non-existing user", "token": ""}
    elif user_type == "0":  # LOGIN ALUMN
        status, res = con.select(table="alumn",
                                 where="email = '"+email+"'")
        if(status == 1):
            if res[0][2] == resource['password']:
                return generate_token(res[0][0], user_type)
            else:
                return {"status": "0", "msg": "Wrong password", "token": ""}
        else:
            return {"status": "2", "msg": "Non-existing user", "token": ""}
    else:
        return {"status": "3", "msg": "Missing Data", "token": ""}
async def logout(request: Request):
    resource = await request.json()
    token = resource['token']
    con.update(table="token",
               values=["expired = '1'"],
               where="id_token = " + token)
    return {"status":800,"Message":"Logged Out"}


# PASSWORD RESET
async def sendRecoverToken(request: Request):
    resource = await request.json()
    print(resource)
    sender = emailSender(sender="therealchalinosanchez@gmail.com", password="mlta vekc irlj exls")
    code = ""
    while True:
        p1 = ''.join(random.choice(characters) for i in range(3))
        p2 = ''.join(random.choice(characters) for i in range(3))
        p3 = ''.join(random.choice(characters) for i in range(3))
        code = p1 + "-" + p2 + "-" + p3
        print(code)
        status, res = con.select(table="verify_token",
                                 where="token = '" + code + "'")
        if len(res) == 0:
            break
    user = ""
    if resource['type'] == "1": #ADMIN
        status, res = con.select(table="admin",
                                 where="email = '" + resource['email'] + "'")
        print(res)
        user = res[0][0]
    if resource['type'] == "0": #ALUMN
        status, res = con.select(table="alumn",
                                 where="email = '" + resource['email'] + "'")
        user = res[0][0]

    expiration_date = datetime.datetime.now() + timedelta(minutes=30)
    print(expiration_date)
    print(user)
    if not user == "":
        status, msg = con.insert(table="verify_token",
                                 fields="token, id_user, type, expiration, expirated",
                                 values=[str(code), str(user), resource['type'], str(expiration_date), "0"])
        print(status,msg)
        if status == 1:
            sender.sendEmail(subject="Recuperacion de contraseña",
                             recipients=[resource['email']],
                             file="pages/assets/index.html",
                             code=code)
            return {"status": "1", "message": "Email sent"}
        else:
            return {"status": "2", "message": "Error while registering token"}
    else:
        return {"status": "0", "message": "Email not registered"}


async def VerifyPasswordToken(request: Request):
    resource = await request.json()
    token = resource['token']
    status, res = con.select(table="verify_token",
                             where="token = '" + token + "'")
    if len(res) > 0:
        expiration_date = parse(str(res[0][4]))
        today = parse(str(date.today()))
        print(today)
        if expiration_date > today:
            return {"status": "1", "message":"Valid Token"}
        else:
            con.update(table="verify_token",
                       values=["expirated = '1'"],
                       where="token = " + str(token))
            return {"status": "2", "message":"Token Expired"}
    else:
        return {"status": "0", "message": "Invalid Expired"}


async def PasswordReset(request: Request):
    resource = await request.json()
    token = resource['token']
    password = resource['password']
    status, res = con.select(table="verify_token",
                             where="token = '" + token + "'")
    user = int(res[0][2])
    type = int(res[0][3])
    exit = 0
    if int(res[0][5]) == 0:
        if type == 1: #ADMIN
            con.update(table="admin",
                       values=["password = '"+password+"'"],
                       where="id_admin = '" + str(user)+"'")
            exit = 1
        if type == 0: #ALUMN
            con.update(table="alumn",
                       values=["password = '"+password+"'"],
                       where="id_alumn = '" + str(user)+"'")
            exit = 1
        if exit == 1:
            con.update(table="verify_token",
                       values=["expirated = '1'"],
                       where="token = '" + str(token)+"'")
            return {"status": "1", "message": "Password Updated"}
    else:
        return {"status": "2", "message": "Token expirated"}
    return {"status": "0", "message": "Error"}


# EMAIL VERIFICATION

async def sendEmailVerification(request: Request):
    resource = await request.json()
    sender = emailSender(sender="therealchalinosanchez@gmail.com", password="mlta vekc irlj exls")
    code = ""
    while True:
        p1 = ''.join(random.choice(characters) for i in range(3))
        p2 = ''.join(random.choice(characters) for i in range(3))
        p3 = ''.join(random.choice(characters) for i in range(3))
        code = p1 + "-" + p2 + "-" + p3
        print(code)
        status, res = con.select(table="verify_email",
                                 where="token = '" + code + "'")
        if len(res) == 0:
            break
    user = ""
    if resource['type'] == "1": #ADMIN
        status, res = con.select(table="admin",
                                 where="email = '" + resource['email'] + "'")
        print(res)
        user = res[0][0]
    if resource['type'] == "0": #ALUMN
        status, res = con.select(table="alumn",
                                 where="email = '" + resource['email'] + "'")
        user = res[0][0]

    expiration_date = datetime.datetime.now() + timedelta(minutes=30)
    print(expiration_date)
    print(user)
    print(resource['type'])
    print(str(code))
    if not user == "":
        status, msg = con.insert(table="verify_email",
                                 fields="token, id_user, type, expiraton, expirated",
                                 values=[str(code), str(user), str(resource['type']), str(expiration_date), "0"])
        print(status,msg)
        if status == 1:
            sender.sendEmail(subject="VERIFICACION DE CORREO",
                             recipients=[resource['email']],
                             file="pages/assets/verify.html",
                             code=code)
            return {"status": "1", "message": "Email sent"}
        else:
            return {"status": "0", "message": "Error while registering token"}
    else:
        return {"status": "0", "message": "Email not registered"}

async def emailVerification(request: Request):
    resource = await request.json()
    token = resource['token']
    status, res = con.select(table="verify_email",
                             where="token = '" + token + "'")
    user = int(res[0][1])
    type = int(res[0][3])
    print(user)
    print(type)
    exit = 0
    if int(res[0][5])==0:
        if type == 1: #ADMIN
            con.update(table="admin",
                       values=["state = '1'"],
                       where="id_admin = " + str(user))
            exit = 1
        if type == 0: #ALUMN
            con.update(table="alumn",
                       values=["password = '1'"],
                       where="id_alumn = " + str(user))
            exit = 1
        if exit == 1:
            con.update(table="verify_email",
                       values=["expirated = '1'"],
                       where="token = '" + str(token)+"'")
            return {"status": "1", "message": "Email verificated"}
    else:
        return {"status": "2", "message": "Token expirated"}
    return {"status": "0", "message": "Error"}

class emailSender:
    sender = ""
    password = ""

    def __init__(self,sender,password):
        self.sender = sender
        self.password = password

    def sendEmail(self, subject, recipients, file, code):
        HTMLFile = open(file, "r", encoding="utf-8")
        index = HTMLFile.read()
        index = index.replace("REPLACE-ME",code)
        msg = MIMEText(index, 'html')
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
           smtp_server.login(self.sender, self.password)
           smtp_server.sendmail(self.sender, recipients, msg.as_string())
        print("Message sent!")

async def log(request: Request):
  resource = await request.json()
  status, res_token = con.custom(
    "SELECT id_user FROM token WHERE token='" + resource['token'] + "'")
  res_token = list(res_token)
  status, res_admin = con.custom(
    "SELECT user FROM admin WHERE id_admin = '" + str(res_token[0][0]) + "'")
  res_admin = list(res_admin)
  status, msg = con.insert(table="log",
                           fields="user, log",
                           values=[res_admin[0][0],resource['log']])
  print(msg)
  return {"status": 200, "message": "Registro exitoso"}
