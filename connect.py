from pymongo import MongoClient

class Connect(object):
    @staticmethod    
    def get_connection():
        #user = os.environ['MDB_USERNAME']
        #password = os.environ['MDB_PASSWORD']
        #mongoLink = os.environ['MDB_LINK']
        return MongoClient("mongodb://admin:Homeslicer1@cluster0-shard-00-00-ftwiq.mongodb.net:27017,cluster0-shard-00-01-ftwiq.mongodb.net:27017,cluster0-shard-00-02-ftwiq.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")