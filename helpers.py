import requests

from main import con
#HELPERS
def repeated(table, field, value):
    sentence = field + "='"+value+"'"
    status, msg = con.repeated(table=table,
                               where=sentence)
    return status

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