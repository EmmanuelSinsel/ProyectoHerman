from SQLConnection import SQLConnector
import requests
con = SQLConnector(host="localhost",
                     db="biblioteca",
                   port="3306",
                   user="root",
               password="piedras123.")
con.connect()

def testInsert():
    #INSERT
    status, msg = con.insert(table="admins",
                             fields="user, password, first_name, last_name, phone, email",
                             values=['admin12345', 'password', 'jesus', 'sinsel', '6681342312', 'user@gmail.com'])
    print(status, msg)

def testSelect():
    #SELECT
    status, res = con.select(table="admins",
                             where="user='admin123'")
    print(res)

def testUpdate():
    #UPDATE
    status, msg = con.update(table="admins",
                             values=["user = 'admin123456'",
                                     "password = 'password123'",
                                     "phone = '6681455667'"],
                             where="id_admin = 4")
    print(msg)

def testDelete():
    status, msg = con.delete(table="admins",
                             where="id_admin = 16")
    print(msg)



#  GOOGLE BOOKS API
def get_book(isbn, title):
    if isbn == "":
        url = 'https://www.googleapis.com/books/v1/volumes?q=title:' + title;
        request = requests.get(url)
        res = request.json()
        title = res['items'][0]['volumeInfo']['title']
        author = res['items'][0]['volumeInfo']['authors'][0]
        return title, author
    if title == "":
        url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn;
        request = requests.get(url)
        res = request.json()
        title = res['items'][0]['volumeInfo']['title']
        author = res['items'][0]['volumeInfo']['authors'][0]
        return title, author


@app.post("/insert_admin")
async def insert_admin(request: models.Admin):
    return Admin.insertNotRepeated(request, "email")

@app.put("/update_admin/{updateValue}")
async def update_admin(updateValue: str, request: models.Admin):
    return Admin.update(request, updateValue)

@app.put("/delete_admin/{where}")
async def delete_admin(where: str):
    return Admin.delete(where)

@app.get("/list_admin/{where}")
async def list_admin(where: str):
    print(where)
    return await Admin.list(where)

@app.get("/list_admin/")
async def list_admin():
    return await Admin.list("")


