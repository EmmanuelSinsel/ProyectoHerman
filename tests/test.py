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
