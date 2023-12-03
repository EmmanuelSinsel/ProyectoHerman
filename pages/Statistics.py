from fastapi import Request
from manager import con

async def get_full_dashboard():

  # SEARCH ALUMN ACCOUNT NUMBER
  query = (
    "SELECT id_category, category from category"
  )
  status, cats = con.custom(query)
  cats = list(cats)

  query = (
    "SELECT YEAR(t.date_transaction) AS year, MONTH(t.date_transaction) AS month,c.id_category, c.category, COUNT(*) AS count"
    " FROM transactions t"
    " JOIN book p ON t.id_book = p.id_book"
    " JOIN category c on p.id_category = c.id_category"
    " GROUP BY YEAR(t.date_transaction), MONTH(t.date_transaction),c.id_category, c.category"
    " ORDER BY YEAR(t.date_transaction), MONTH(t.date_transaction);"
  )
  status, res = con.custom(query)
  data = list(res)
  response = {}
  for i in range(1,13):
    month = {}
    for k in range(len(cats)):
      month[cats[k][0]]= {"id_category":cats[k][0],"category":cats[k][1], "count":0}
    for j in range(len(data)):
      if(int(data[j][1])==i):
        cat = {
          "id_category": data[j][2],
          "category": data[j][3],
          "count": data[j][4]
        }
        month[data[j][2]] = cat
    response[str(i)] = month
  response = {
    "categories":cats,
    "data":response
  }
  return response
