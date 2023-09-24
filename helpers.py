from main import con
#HELPERS
def repeated(table, field, value):
    sentence = field + "='"+value+"'"
    status, msg = con.repeated(table=table,
                               where=sentence)
    return status