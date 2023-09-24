from SQLConnection import SQLConnector

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
testDelete()