import os
from pymongo import MongoClient

class Connect(object):
    @staticmethod    
    def get_connection():
        user = os.environ['MDB_USERNAME']
        password = os.environ['MDB_PASSWORD']
        mongoLink = os.environ['MDB_LINK']
        return MongoClient("mongodb+srv://"+user+":"+password+"@"+mongoLink)
