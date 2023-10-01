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
            break
    expiration_date = date.today()+ timedelta(days=token_expiration_time)
    print(id_user, type_user, token, expiration_date)
    con.insert(table="TOKEN",
               fields="id_user, type_user, token, expiration_date, expired",
               values=[str(id_user), str(type_user), str(token), str(expiration_date), "0"])
    return {"status": "1", "msg": "Sucessful login", "token": token}


def Authenticate(token):
    status, res = con.select(table="TOKEN",
                             where="token = '" + token + "'")
    if(len(res)>0):
        if res[0][5] == "0":
            expiration_date = parse(str(res[0][4]))
            today = parse(str(date.today()))
            if expiration_date > today:
                print("Authentication Succesful")
                return True
            else:
                con.update(table="TOKEN",
                           values=["expired = '1'"],
                           where="id_token = "+res[0][0])
                print("Authentication Failed")
                return False
        if res[0][5] == "1":
            print("Authentication Failed")
            return False

# AUTHENTICATION
async def login(request: models.Login):
    resource = request.dict()
    if not resource['token'] == "":
        if Authenticate(resource['token']):
            return {"status": "400", "msg": "Valid token", "token": "", "type": resource['type']}
        else:
            return {"status": "500", "msg": "Invalid token", "token": "", "type": resource['type']}
    user_type = resource["type"]
    email = resource["email"]
    if user_type == "1" and not email == "":  # LOGIN ADMIN
        status, res = con.select(table="ADMIN",
                                 where="email = '"+email+"'")
        print(res)
        if(status == 1):
            if res[0][2] == resource['password']:
                return generate_token(res[0][0], user_type)
            else:
                return {"status": "0", "msg": "Wrong password", "token": ""}
        else:
            return {"status": "2", "msg": "Non-existing user", "token": ""}
    elif user_type == "0":  # LOGIN ALUMN
        status, res = con.select(table="ALUMN",
                                 where="email = '"+email+"'")
        if(status == 1):
            if res[0][2] == resource['password']:
                return generate_token(res[0][0], user_type)
            else:
                return {"status": "0", "msg": "Wrong password", "token": ""}
        else:
            return {"status": "2", "msg": "Non-existing user", "token": ""}
    else:
        return {"status": "1", "msg": "Missing Data", "token": ""}
async def logout(request):
    return 0
