import json
import psycopg2 as dbl

class Database():
    def __init__(self):
        """initialize psql database with config"""

    @staticmethod
    def getconnection():
        try:
            connection = dbl.connect(dbname='llin15', user='llin15')
        except (Exception, dbl.DatabaseError) as e:
            print("Connection error")
            print(e)
        return connection
