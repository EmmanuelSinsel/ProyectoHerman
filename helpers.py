import requests
from difflib import SequenceMatcher
import json
from fastapi import Request

from manager import con
#HELPERS
def repeated(table, field, value):
    sentence = field + "='"+value+"'"
    status, msg = con.repeated(table=table,
                               where=sentence)
    return status

def get_fields(table):
    data = con.fields(table)
    return data

def get_book(isbn, title):
    if isbn == "":
        url = 'https://www.googleapis.com/books/v1/volumes?q=title:' + title;
        request = requests.get(url)
        res = request.json()
        similarity = 0
        title = ""
        author = ""
        for i in range(len(res['items'][0])):
            temp = compute_similarity(res['items'][i]['volumeInfo']['title'], title)
            print(res['items'][i]['volumeInfo']['title'] + " : " + str(temp))
            if similarity == 0 or temp >= similarity:
                similarity = temp
                title = res['items'][i]['volumeInfo']['title']
                author = res['items'][i]['volumeInfo']['authors'][0]
                isbn = res['items'][i]['volumeInfo']['industryIdentifiers'][0]['identifier']
        print("--------------------------------------------------------------------------------------")
        print(res['items'][i]['volumeInfo']['title'] + " : " + str(similarity))
        return {"title": title, "author": author, "isbn" : isbn}
    if title == "":
        url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn;
        request = requests.get(url)
        res = request.json()
        title = res['items'][0]['volumeInfo']['title']
        author = res['items'][0]['volumeInfo']['authors'][0]
        return {"title": title, "author": author}


def levenshtein_distance(s, t):
    m, n = len(s), len(t)
    if m < n:
        s, t = t, s
        m, n = n, m
    d = [list(range(n + 1))] + [[i] + [0] * n for i in range(1, m + 1)]
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1]) + 1
    return d[m][n]


def compute_similarity(input_string, reference_string):
    distance = levenshtein_distance(input_string, reference_string)
    max_length = max(len(input_string), len(reference_string))
    similarity = 1 - (distance / max_length)
    return similarity


async def get_admin_profile(request:Request):
  res = await request.json()
  print(res)
  query = (
    "SELECT id_user from token WHERE token = '"+res['token']+"'"
  )
  status, token = con.custom(query)
  token = list(token)

  query = (
    "SELECT * from admin WHERE id_admin = '"+str(token[0][0])+"'"
  )
  status, admin = con.custom(query)
  admin = list(admin)
  admin_profile = {
    "id":admin[0][0],
    "user": admin[0][1],
    "password": admin[0][2],
    "first_name": admin[0][3],
    "last_name": admin[0][4],
    "phone": admin[0][5],
    "email": admin[0][6],
    "state": admin[0][7],
    "library_id": admin[0][8],
    "master":admin[0][9]
  }
  return {"profile":admin_profile}

async def get_alumn_profile(request:Request):
  res = await request.json()
  print(res)
  query = (
    "SELECT id_user from token WHERE token = '"+res['token']+"'"
  )
  status, token = con.custom(query)
  token = list(token)

  query = (
    "SELECT * from alumn WHERE id_alumn = '"+str(token[0][0])+"'"
  )
  status, alumn = con.custom(query)
  alumn = list(alumn)
  alumn_profile = {
    "id":alumn[0][0],
    "account_number": alumn[0][1],
    "user": alumn[0][2],
    "password":alumn[0][3],
    "school_group": alumn[0][4],
    "carreer": alumn[0][5],
    "first_name": alumn[0][6],
    "last_name": alumn[0][7],
    "phone": alumn[0][8],
    "email": alumn[0][9],
    "last_preference": alumn[0][10],
    "state": alumn[0][11],
    "library_id": alumn[0][12]
  }
  return {"profile":alumn_profile}
