import datetime

import mysql
from mysql.connector import Error
class SQLConnector:
    con = None
    cur = None
    SQL_HOST = ""
    SQL_DB = ""
    SQL_PORT = ""
    SQL_USER = ""
    SQL_PASSWORD = ""

    def __init__(self, host, db, port, user, password):
        self.SQL_HOST = host
        self.SQL_DB = db
        self.SQL_PORT = port
        self.SQL_USER = user
        self.SQL_PASSWORD = password

    def connect(self):
        self.con = mysql.connector.connect(
            host=self.SQL_HOST,
            user=self.SQL_USER,
            password=self.SQL_PASSWORD,
            database=self.SQL_DB
        )
        self.cur = self.con.cursor()

    #JALA AL 100
    def delete(self, table, where):
        query = "DELETE FROM "+ table +" WHERE " + where
        self.con.cursor.execute(query)
        self.con.commit()
        if self.con.cursor.rowcount >= 1:
            return 1, "Succesful delete"
        else:
            return 0, "Error while deleting values"
    #JALA AL 100
    def insert(self, table, fields, values):
        cursors = ""
        for i in values:
            if type(i) is str:
                cursors += "%s, "
            if type(i) is None:
                cursors += "%s, "
            if type(i) is float:
                cursors += "%f, "
            if type(i) is int:
                cursors += "%i, "
            if type(i) is datetime.date:
                cursors += "'%s', "
        cursors = cursors[:-2]
        try:
            query = "INSERT INTO " + table + " (" + fields + ") VALUES (" + cursors + ")"
            self.cur.execute(query, values)
            self.con.commit()
            if self.cur.rowcount >= 1:
              return 200, "Succesful insert"
            else:
              return 400, "Error while inserting values"
        except Error as e:
          return 0, e

    #JALA Al 100
    def update(self, table, values, where):
      sets = ""
      for i in values:
        sets += i+", "
      sets = sets[:-2]
      query = "UPDATE " + table + " SET " + sets + " WHERE "+ where
      self.cur.execute(query)
      self.con.commit()
      if self.cur.rowcount >= 1:
        return 200, "Succesful update"
      else:
        return 400, "Error while updating values"

    #JALA AL 100
    def select(self, table, where):
      if(not where == ""):
          query = "SELECT * FROM "+ table +" WHERE "+where
      else:
          query = "SELECT * FROM " + table
      self.cur.execute(query)
      return 200, self.cur.fetchall()

    #HELPERS
    def fields(self, table):
        query = "SHOW COLUMNS FROM "+table+";"
        self.cur.execute(query)
        columns = [column[0] for column in self.cur.description]
        data = [dict(zip(columns, row)) for row in self.cur.fetchall()]
        return data
    def repeated(self, table, where):
        query = "SELECT COUNT(*) FROM "+ table +" WHERE "+where+""
        self.cur.execute(query)
        result = self.cur.fetchone()
        row_count = result[0]
        if(row_count > 0):
            return 200, "Repeated" #REPEATED
        if(row_count == 0):
            return 400, "Not repeated" #NOT REPEATED

    def custom(self, query):
      self.cur.execute(query)
      return 200, self.cur.fetchall()
