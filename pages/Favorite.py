from main import con, converter
from helpers import repeated
import models
table = "FAVORITE"
#FAVORITOS
def add_favorite(request: models.Favorite):
    fields, values = converter.insert(request)
    status, msg = con.insert(table=table,
                             fields=fields,
                             values=values)
    return {"message": msg, "status": status}
def remove_favorite(request: models.Where):
    res = request.dict()
    status, msg = con.update(table=table,
                             values=["state = 0"],
                             where=res['where'])
    return {"message": msg, "status": status}