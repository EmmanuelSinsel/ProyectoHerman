import json
import random
import string
from datetime import date, datetime, timedelta
from main import con, converter
from helpers import repeated
import models
from dateutil.parser import parse

# TOKENS

token_expiration_time = 30  # DIAS

def generate_token(id_user, type_user):
    flag = 0
    while flag == 0:
        characters = string.ascii_letters + string.digits
        token = ''.join(random.choice(characters) for i in range(30))
        print("Generated Token: "+token)

        status, res = con.select(table="TOKEN",
                                 where="token = '" + token + "'")
        if len(res) == 0:
            flag = 1
            break
    expiration_date = date.today()+ timedelta(days=token_expiration_time)
    print(id_user, type_user, token, expiration_date)
    con.insert(table="TOKEN",
               fields="id_user, type_user, token, expiration_date",
               values=[str(id_user), str(type_user), str(token), str(expiration_date)])
    return {"status": "1", "msg": "Sucessful login", "token": token}


def Authenticate(token):
    status, res = con.select(table="TOKEN",
                             where="token = '" + token + "'")
    expiration_date = ""
    today = ""
    if(len(res)>0):
        expiration_date = parse(str(res[0][4]))
        today = parse(str(date.today()))

    if expiration_date > today:
        print("Authentication Succesful")
        return True
    else:
        print("Authentication Failed")
        return False

# AUTHENTICATION
async def login(request):
    res = await request.json()
    data = res['data']
    if not res['token'] == "":
        if Authenticate(res['token']):
            return {"status": "400", "msg": "Valid token", "token": "", "type": res['type']}
        else:
            return {"status": "500", "msg": "Invalid token", "token": "", "type": res['type']}
    user_type = res["type"]
    if user_type == "1":  # LOGIN ADMIN
        status, res = con.select(table="ADMIN",
                                 where="email = '"+data['email']+"'")
        if(len(res)>0):
            if res[0][2] == data['password']:
                return generate_token(res[0][0], user_type)
            else:
                return {"status": "0", "msg": "Wrong password", "token": ""}
        else:
            return {"status": "2", "msg": "Non-existing user", "token": ""}
    if user_type == "0":  # LOGIN ALUMN
        status, res = con.select(table="ALUMN",
                                 where="email = '"+data['email']+"'")
        if(len(res)>0):
            if res[0][2] == data['password']:
                return generate_token(res[0][0], user_type)
            else:
                return {"status": "0", "msg": "Wrong password", "token": ""}
        else:
            return {"status": "2", "msg": "Non-existing user", "token": ""}

async def logout(request):
    return 0
