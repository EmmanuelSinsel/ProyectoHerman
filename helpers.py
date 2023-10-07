import requests
from difflib import SequenceMatcher

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