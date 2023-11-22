from fastapi import Request
from manager import con


async def get_full_loan(request: Request):
  res = await request.json()
  where = res['where']
  # SEARCH ALUMN ACCOUNT NUMBER
  if not where == "*":
    query = (
      "SELECT transactions.id_transaction,alumn.account_number, book.isbn, book.tittle, transactions.date_transaction, "
      "transactions.date_deadline, transactions.date_return FROM transactions INNER JOIN book "
      "ON transactions.id_book = book.id_book INNER JOIN alumn ON transactions.id_alumn = alumn.id_alumn "
      "WHERE alumn.account_number = '"+where+"'")
  else:
    query = (
      "SELECT transactions.id_transaction,alumn.account_number, book.isbn, book.tittle,transactions.date_transaction, "
      "transactions.date_deadline, transactions.date_return FROM transactions INNER JOIN book "
      "ON transactions.id_book = book.id_book INNER JOIN alumn ON transactions.id_alumn = alumn.id_alumn")
  status, res = con.custom(query)
  data = list(res)
  response = {}
  for i in range(len(data)):
    row = {
      'id_transaction': data[i][0],
      'account_number': data[i][1],
      'isbn': data[i][2],
      'book': data[i][3],
      'date_transaction': data[i][4],
      'date_deadline': data[i][5],
      'date_return': data[i][6]
    }
    response[str(i)] = row
  return response


async def register_loan(request: Request):
  resource = await request.json()
  status, res_alumn = con.select(table="alumn",
                                 where="account_number = '" + resource['account'] + "'")
  status, res_book = con.select(table="book",
                                where="isbn = '" + resource['isbn'] + "'")
  status, res_admin = con.custom(
    "SELECT admin.library_id FROM admin INNER JOIN token ON token.token='" + resource['token'] + "'")
  id_alumn = ""
  id_book = ""
  id_library = ""
  if len(res_admin) > 0:
    data = list(res_admin)
    id_library = data[0][0]
  else:
    return {"status": 400, "message": "Token inexistente"}
  if len(res_alumn) > 0:
    data = list(res_alumn)
    id_alumn = data[0][0]
  else:
    return {"status": 401, "message": "Alumno inexistente"}
  if len(res_book) > 0:
    data = list(res_book)
    id_book = data[0][0]
    if data[0][5] == '0':
      return {"status": 403, "message": "Libro prestado"}
  else:
    return {"status": 402, "message": "Libro inexistente"}
  status, msg = con.insert(table="transactions",
                           fields="id_alumn, id_book, date_transaction, date_deadline, notation, id_library, state",
                           values=[str(id_alumn), str(id_book), resource['date_transaction'], resource['date_deadline'],
                                   resource['notation'],str(id_library),resource['state']])
  print(msg)
  status, msg = con.update(table="book",
                           values=[
                                   "status = 0",
                                   ],
                           where="id_book = '"+str(res_book[0][0])+"'")
  return {"status": 200, "message": "Registro exitoso"}

async def update_loan(request: Request):
  resource = await request.json()
  status, res_alumn = con.select(table="alumn",
                                 where="account_number = '" + resource['account'] + "'")
  status, res_book = con.select(table="book",
                                where="isbn = '" + resource['isbn'] + "'")
  status, res_transaction = con.select(table="transactions",
                                       where="id_transaction = '"+str(resource['where'])+"'")
  status, res_admin = con.custom(
    "SELECT admin.library_id FROM admin INNER JOIN token ON token.token='" + resource['token'] + "'")
  id_alumn = ""
  id_book = ""
  id_library = ""
  if len(res_admin) > 0:
    data = list(res_admin)
    id_library = data[0][0]
  else:
    return {"status": 400, "message": "Token inexistente"}
  if len(res_alumn) > 0:
    data = list(res_alumn)
    id_alumn = data[0][0]
  else:
    return {"status": 401, "message": "Alumno inexistente"}
  if len(res_book) > 0:
    data = list(res_book)
    id_book = data[0][0]
    if data[0][5] == '0' and (not res_transaction[0][2] == res_book[0][0]):
      return {"status": 403, "message": "Libro prestado"}
  else:
    return {"status": 402, "message": "Libro inexistente"}

  status, msg = con.update(table="transactions",
                           values=["id_alumn = '"+str(id_alumn)+"'",
                                   "id_book = '"+str(id_book)+"'",
                                   "date_transaction = '"+resource['date_transaction']+"'",
                                   "date_deadline = '"+resource['date_deadline']+"'",
                                   "notation = '"+resource['notation']+"'",
                                   "id_library = '"+str(id_library)+"'",
                                   "state = '"+resource['state']+"'",
                                   ],
                           where="id_transaction = '"+str(resource['where'])+"'")
  return {"status": 200, "message": "Registro exitoso"}

async def get_book_data(request: Request):
  resource = await request.json()
  status, res = con.custom("SELECT book.tittle, category.category, author.name, book.status, book.id_book FROM book "
                           "INNER JOIN category ON book.id_category = category.id_category "
                           "INNER JOIN author ON author.id_author = book.id_author WHERE isbn = '"+resource['isbn']+"'")

  if len(res) > 0:
    response = {
      'title':res[0][0],
      'category':res[0][1],
      'author':res[0][2],
      'status':res[0][3],
      'id_book':res[0][4]
    }
    return {"0":response}
  return {"status": 402, "message": "Libro inexistente"}

