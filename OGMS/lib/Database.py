import json
import psycopg2 as dbl

class Database():
    def __init__(self):
        """initialize psql database with config"""

    @staticmethod
    def getconnection():
        try:
            connection = dbl.connect(dbname='lina_sample_db_project', user='lina')
        except (Exception, dbl.DatabaseError) as e:
            print("Connection error")
            print(e)
        return connection
