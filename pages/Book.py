from fastapi import Request
from manager import con


async def get_full_book(request: Request):
  res = await request.json()
  arg_count = 0
  # SEARCH ALUMN ACCOUNT NUMBER
  query = ("SELECT book.id_book, book.tittle, book.isbn, category.category, author.name, book.status "
           "FROM book INNER JOIN category ON category.id_category = book.id_category "
           "INNER JOIN author ON author.id_author = book.id_author ")
  if(res['author'] != "*" or res["category"] != "*" or res["title"] != "*" or res["isbn"] != "*"):
    query += "WHERE "
    if(res['author'] != "*"):
      if(arg_count>0):query+=" AND "
      query += "author.name LIKE '"+res['author']+"%'"
      arg_count += 1
    if(res['category'] != "*"):
      if(arg_count>0):query+=" AND "
      query += "category.category LIKE '"+res['category']+"%'"
      arg_count += 1
    if(res['title'] != "*"):
      if(arg_count>0):query+=" AND "
      query += "book.tittle LIKE '"+res['title']+"%'"
      arg_count += 1
    if(res['isbn'] != "*"):
      if(arg_count>0):query+=" AND "
      query += "book.isbn LIKE '"+res['isbn']+"%'"
      arg_count += 1
  if(arg_count == 0):
    query += "WHERE book.state = '1'"
  else:
    query += "AND book.state = '1'"
  print(query)
  status, res = con.custom(query)
  data = list(res)
  response = {}
  for i in range(len(data)):
    row = {
      'id_book': data[i][0],
      'title': data[i][1],
      'isbn': data[i][2],
      'category': data[i][3],
      'author': data[i][4],
      'stock': data[i][5]
    }
    response[str(i)] = row
  return response


async def register_book(request: Request):
  resource = await request.json()
  status, res_author = con.select(table="author",
                                 where="name = '" + resource['author'] + "'")
  status, res_category= con.select(table="category",
                                where="category = '" + resource['category'] + "'")
  status, res_book= con.select(table="book",
                                where="isbn = '" + resource['isbn'] + "' AND state = 1")
  status, res_admin = con.custom(
    "SELECT admin.library_id FROM admin INNER JOIN token ON token.token='" + resource['token'] + "'")
  id_author = ""
  id_category = ""
  id_library = ""
  book_count = 0
  if len(res_admin) > 0:
    data = list(res_admin)
    id_library = data[0][0]
  else:
    return {"status": 400, "message": "Token inexistente"}
  if len(res_author) > 0:
    data = list(res_author)
    id_author = data[0][0]
  else:
    return {"status": 401, "message": "Alumno inexistente"}
  if len(res_category) > 0:
    data = list(res_category)
    id_category = data[0][0]
  if len(res_book) > 0:
    return {"status": 402, "message": "Libro ya registrado"}
  status, msg = con.insert(table="book",
                           fields="tittle, isbn, id_category, id_author, status, image, id_library, state",
                           values=[resource['title'], resource['isbn'], str(id_category), str(id_author),
                                   str(resource['stock']),"",str(id_library),"1"])
  return {"status": 200, "message": "Registro exitoso"}

async def update_book(request: Request):
  resource = await request.json()
  status, res_author = con.select(table="author",
                                 where="name = '" + resource['author'] + "'")
  status, res_category= con.select(table="category",
                                where="category = '" + resource['category'] + "'")
  status, res_book= con.select(table="book",
                                where="isbn = '" + resource['isbn'] + "'")
  status, actual_book= con.select(table="book",
                                where="id_book = '" + str(resource['where']) + "' AND state = 1")
  status, res_admin = con.custom(
    "SELECT admin.library_id FROM admin INNER JOIN token ON token.token='" + resource['token'] + "'")
  id_author = ""
  id_category = ""
  id_library = ""
  book_count = 0
  if len(res_admin) > 0:
    data = list(res_admin)
    id_library = data[0][0]
  else:
    return {"status": 400, "message": "Token inexistente"}
  if len(res_author) > 0:
    data = list(res_author)
    id_author = data[0][0]
  else:
    return {"status": 401, "message": "Alumno inexistente"}
  if len(res_category) > 0:
    data = list(res_category)
    id_category = data[0][0]
  if len(res_book) > 0 and res_book[0][2] != str(actual_book[0][2]):
    return {"status": 402, "message": "Libro ya registrado"}
  status, msg = con.update(table="book",
                           values=["tittle = '"+str(resource['title'])+"'",
                                   "isbn = '"+str(resource['isbn'])+"'",
                                   "id_category = '"+str(id_category)+"'",
                                   "id_author = '"+str(id_author)+"'",
                                   ],
                           where="id_book = '"+str(resource['where'])+"'")
  return {"status": 200, "message": "Registro exitoso"}
