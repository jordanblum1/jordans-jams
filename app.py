import os
from flask import Flask, request, session, render_template
from connect import Connect
from twilio.twiml.messaging_response import MessagingResponse
from jordansJams import verify, add_songs, get_jams, clear_songs, is_subscriber, new_user, remove_user, default_message

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.config.from_object(__name__)

mongo = Connect.get_connection()
numbers = mongo.jordansJams.numbers


@app.route('/')
def index():
    '''renders homepage'''
    return render_template('jordansJams.html')


@app.route('/addFromWeb/<number>', methods=['POST'])
def web_add(number):
    '''adds subscriber from the web'''
    if is_subscriber(number):
        return "Error: Number already subscribed to Jordan's Jams"
    else:
        return new_user(number)


@app.route('/jams', methods=['POST'])

def sms():
    '''used for all communications of text'''
    resp = MessagingResponse()
    number = request.form['From']
    inbound_message = (request.form['Body'])

    counter = session.get('counter', 0)
    counter += 1
    session['counter'] = counter

    print(inbound_message)
    print(counter)

    exit_words = ["STOP", "END", "UNSUBSCRIBE", "REMOVE"]
    if inbound_message.upper() in exit_words:
        return remove_user(number)

    if inbound_message == "CLEAR":
        session['counter'] = 0
        return clear_songs(number)
    if inbound_message == "JAMS":
        return get_jams(number)
    if (inbound_message == "ADD") or (counter >= 1 and "open.spotify.com" in inbound_message.lower()):
        if verify(number):
            return add_songs(number, inbound_message, counter)
    if not is_subscriber(number):
        return new_user(number)
    if is_subscriber(number):
        return default_message(number)

    message_body = 'Error, that is not a possible entry.'
    resp.message(message_body)
    return str(resp)


if __name__ == '__main__':
    app.run(debug=True)
