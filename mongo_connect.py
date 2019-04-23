from flask import Flask, request
from flask_pymongo import PyMongo
from twilio.twiml.messaging_response import Message, MessagingResponse


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'connect_to_mongo'
app.config["MONGO_URI"] = "mongodb+srv://admin:Homeslicer1@cluster0-ftwiq.mongodb.net/test?retryWrites=true"
mongo = PyMongo(app)


#insert
@app.route('/add')
def add():
    user = mongo.db.users
    user.insert({'name': 'Jordan', 'language': 'Python'})
    user.insert({'name': 'Timothy', 'language': 'C'})
    user.insert({'name': 'Pam', 'language': 'Java'})
    user.insert({'name': 'Michael', 'language': 'Pascal'})
    return 'Added user!'

@app.route('/find')
def find():
    user = mongo.db.users
    Jordan = user.find_one({'name': 'Jordan'})
    return 'You found ' + Jordan['name'] + '. His favorite language is ' + Jordan['language']

@app.route('/update')
def update():
    user = mongo.db.users
    pam = user.find_one({'name': 'Pam'})
    pam['language'] = 'Javascript'
    user.save(pam)
    return 'Updated Pam!'

@app.route('/delete')
def delete():
    user = mongo.db.users
    timothy = user.find_one({'name': 'Timothy'})
    user.remove(timothy)
    return 'Removed Timothy'

@app.route('/sms', methods=['POST'])
def sms():
    keyword = request.form['Body']
    return {
        'SUBSCRIBE': newUser()
        'ADD SONGS': initiateSongs()
    }[keyword]

if __name__ == '__main__':
    app.run(debug=True)

#start ngrok server: ngrok http 5000
#start python server: Python mongo_conect.py
#Twilio app should be up and running after that