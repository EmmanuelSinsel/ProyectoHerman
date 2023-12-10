from fastapi import Request
from manager import con

async def get_full_reserves(request: Request):
  res = await request.json()
  where = res['where']
  # SEARCH ALUMN ACCOUNT NUMBER
  if not where == "*":
    query = (
      "SELECT reserves.id_reserve,alumn.account_number, book.isbn, book.tittle, reserves.date_pickup, "
      "reserves.state FROM reserves INNER JOIN book "
      "ON reserves.id_book = book.id_book INNER JOIN alumn ON reserves.id_alumn = alumn.id_alumn "
      "WHERE "+where)
  else:
    query = (
      "SELECT reserves.id_reserve,alumn.account_number, book.isbn, book.tittle, reserves.date_pickup, "
      "reserves.state FROM reserves INNER JOIN book "
      "ON reserves.id_book = book.id_book INNER JOIN alumn ON reserves.id_alumn = alumn.id_alumn")
  print(query)
  status, res = con.custom(query)
  data = list(res)
  response = {}
  for i in range(len(data)):
    row = {
      'id_reserve': data[i][0],
      'account_number': data[i][1],
      'isbn': data[i][2],
      'book': data[i][3],
      'date_pickup': data[i][4],
      'state':data[i][5]
    }
    response[str(i)] = row
  return response

async def deliver_book(request: Request):
  pass
