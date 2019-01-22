import json
import psycopg2 as dbl

class Database():
    def __init__(self):
    """initialize psql database with config"""
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        self.connection = dbl.connect(**config)

    def getconnection(self):
        return self.connection
