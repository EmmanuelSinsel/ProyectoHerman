from main import con, converter
from helpers import repeated
import models

table = "LOG"

def insert_log(user, log):

    status, msg = con.insert(table=table,
                            fields="id_user, log",
                             values=[user, log])
    return {"message": msg,"status":status}
