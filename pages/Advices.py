from fastapi import Request
from manager import con


async def get_full_advice(request: Request):
  res = await request.json()
  where = res['where']
  # SEARCH ALUMN ACCOUNT NUMBER
  if not where == " state = 1":
    query = (
      "SELECT advice.id_advice, alumn.account_number ,advice.message "
      "FROM advice INNER JOIN alumn "
      "ON alumn.id_alumn = advice.id_alumn "
      "WHERE " + where
    )
  else:
    query = (
      "SELECT advice.id_advice, alumn.account_number ,advice.message "
      "FROM advice INNER JOIN alumn "
      "ON alumn.id_alumn = advice.id_alumn ")
  status, res = con.custom(query)
  data = list(res)
  response = {}
  for i in range(len(data)):
    row = {
      'id_advice': data[i][0],
      'account_number': data[i][1],
      'advice': data[i][2]
    }
    response[str(i)] = row
  return response

async def register_advice(request: Request):
  resource = await request.json()
  status, res_alumn = con.select(table="alumn",
                                 where="account_number = '" + resource['alumn'] + "'")
  id_alumn = ""
  if len(res_alumn) > 0:
    data = list(res_alumn)
    id_alumn = data[0][0]
  else:
    return {"status": 401, "message": "Alumno inexistente"}
  status, msg = con.insert(table="advice",
                           fields="id_alumn, message, state",
                           values=[str(id_alumn), resource['advice'],"1"])
  return {"status": 200, "message": "Registro exitoso"}

async def update_advice(request: Request):
  resource = await request.json()
  status, res_alumn = con.select(table="alumn",
                                 where="account_number = '" + resource['account'] + "'")
  id_alumn = ""
  id_book = ""
  id_library = ""
  if len(res_alumn) > 0:
    data = list(res_alumn)
    id_alumn = data[0][0]
  else:
    return {"status": 401, "message": "Alumno inexistente"}

  status, msg = con.update(table="advice",
                           values=["id_alumn = '"+str(id_alumn)+"'",
                                   "message = '"+resource['message']+"'",
                                   "state = '"+resource['state']+"'",
                                   ],
                           where="id_advice = '"+str(resource['where'])+"'")
  return {"status": 200, "message": "Registro exitoso"}
