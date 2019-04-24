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