from SQLConnection import SQLConnector

con = SQLConnector(host="localhost", db="biblioteca", port="3306", user="root", password="")
con.connect()