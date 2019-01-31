import json
import psycopg2 as dbl

class Database():
    @staticmethod
    def getconnection():
        try:
            connection = dbl.connect(dbname='bhashithe', user='bhashithe')
        except (Exception, dbl.DatabaseError) as e:
            print("Connection error")
            print(e)
        return connection
