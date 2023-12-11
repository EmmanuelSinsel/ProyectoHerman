from datetime import timedelta, date

from fastapi import Request
from manager import con
from pages.Auth import emailSender
from dateutil.parser import parse

async def get_full_loan(request: Request):
  res = await request.json()
  where = res['where']
  # SEARCH ALUMN ACCOUNT NUMBER
  if not where == "*":
    query = (
      "SELECT transactions.id_transaction,alumn.account_number, book.isbn, book.tittle, transactions.date_transaction, "
      "transactions.date_deadline, transactions.date_return, transactions.notation FROM transactions INNER JOIN book "
      "ON transactions.id_book = book.id_book INNER JOIN alumn ON transactions.id_alumn = alumn.id_alumn "
      "WHERE "+where+" ORDER BY transactions.id_transaction")
  else:
    query = (
      "SELECT transactions.id_transaction,alumn.account_number, book.isbn, book.tittle,transactions.date_transaction, "
      "transactions.date_deadline, transactions.date_return, transactions.notation FROM transactions INNER JOIN book "
      "ON transactions.id_book = book.id_book INNER JOIN alumn ON transactions.id_alumn = alumn.id_alumn ORDER BY transactions.id_transaction")

  print(query)
  status, res = con.custom(query)
  data = list(res)
  print(data)
  response = {}
  for i in range(len(data)):
    row = {
      'id_transaction': data[i][0],
      'account_number': data[i][1],
      'isbn': data[i][2],
      'book': data[i][3],
      'date_transaction': data[i][4],
      'date_deadline': data[i][5],
      'date_return': data[i][6],
      'notation': data[i][7]
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
  book_count = 0
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
    book_count = data[0][5]
    if int(data[0][5]) == 0:
      return {"status": 403, "message": "Libro prestado"}
  else:
    return {"status": 402, "message": "Libro inexistente"}
  status, msg = con.insert(table="transactions",
                           fields="id_alumn, id_book, date_transaction, date_deadline, notation, id_library, state",
                           values=[str(id_alumn), str(id_book), resource['date_transaction'], resource['date_deadline'],
                                   resource['notation'],str(id_library),resource['state']])
  print("count:", book_count)
  status, msg = con.update(table="book",
                           values=[
                                   "status = "+str(int(book_count)-1),
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
    today = parse(str(date.today()))
    if(parse(str(data[0][13]))!= None):
      if(parse(str(data[0][13]))>today):
        return {"status": 401, "message": "El Alumno tiene una penalizacion hasta el dia: "+str(data[0][13])}
      else:
        status, msg = con.update(table="alumn",
                                 values=["timeout = NULL", ],
                                 where="id_alumn = '" + str(resource['alumn']) + "'")
  else:
    return {"status": 401, "message": "Alumno inexistente"}
  if len(res_book) > 0:
    data = list(res_book)
    id_book = data[0][0]
    if int(data[0][5]) == 0 and (not res_transaction[0][2] == res_book[0][0]):
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

async def check_timeout(request: Request):
  resource = await request.json()
  date = parse(str(resource['date']))
  today = parse(str(date.today()))
  if(today>date):
    expiration_date = date.today() + timedelta(days=7)
    status, msg = con.update(table="alumn",
                             values=["timeout = '" + str(expiration_date) + "'",],
                             where="id_alumn = '" + str(resource['alumn']) + "'")
    return {"status":"1", "message":msg}
  else:
    return {"status":"0","message":"No timeout"}

async def get_book_data(request: Request):
  resource = await request.json()
  status, res = con.custom("SELECT book.tittle, category.category, author.name, book.status, book.id_book FROM book "
                           "INNER JOIN category ON book.id_category = category.id_category "
                           "INNER JOIN author ON author.id_author = book.id_author WHERE isbn = '"+resource['isbn']+"'")
  print(res)
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


async def send_return_mail(request: Request):
  resource = await request.json()
  code = resource['title']
  sender = emailSender(sender="therealchalinosanchez@gmail.com", password="mlta vekc irlj exls")
  sender.sendEmail(subject="VERIFICACION DE CORREO",
                   recipients=[resource['email']],
                   file="pages/assets/return.html",
                   code=code)

