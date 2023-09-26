from main import con, converter
from helpers import repeated
import models

#TOKENS

def generate_token(user):
    token = ""
    return token

def check_token(token):
    return 1



#ADMINS
async def login(request):
    res = await request.json()
    data = res['data']
    if(res["type"]=="1"):
        status, res = con.select(table="ADMIN",
                                 where="WHERE email='"+data['email']+"'")
        if res[0]["password"] == data["password"]:
            return 1
        else:
            return 0

async def logout(request):
    return 0
