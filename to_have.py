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




#Create a response to text back w/ twiml
    resp = MessagingResponse()

    #open up number database and add phone number
    numbers = mongo.db.numbers
    number = request.form['From']

    #try to add the number, if it already exists then
    #send a message back that they are already subscribed
    #
    #If not, then add them 
    try:
        numbers.insert({'_id': request.form['From']})
    except:
        message_body = 'You are already subscribed to Jordan\'s Jams. Look out for new songs to come!'
        resp.message(message_body)
        return str(resp)
    message_body = 'Thanks for subscribing to Jordan\'s Jams. Text TUNES if you would like this weeks currently songs.'
    resp.message(message_body)