from flask import Flask, render_template, request, session
import cgi
import datetime
import time
import json

app = Flask(__name__)

#Settings
app.config['DEBUG'] = True
app.config['PUSHER_CHAT_APP_ID'] = '201277'
app.config['PUSHER_CHAT_APP_KEY'] = 'b54b54f2a70e40232b02'
app.config['PUSHER_CHAT_APP_SECRET'] = '4ea61a6cd96e2748624f'
app.config['PUSHER_CHAT_APP_CLUSTER'] = 'eu'
app.config['SECRET_KEY'] = '\xe9L\x0b\x16\x91\xac\x07NQU,U\xd4w\x82\xe0\x8e\x94\xc0\x8cY-\x12x'

import pusher

pusher_client = pusher.Pusher(
  app_id=app.config['PUSHER_CHAT_APP_ID'],
  key=app.config['PUSHER_CHAT_APP_KEY'],
  secret=app.config['PUSHER_CHAT_APP_SECRET'],
  cluster=app.config['PUSHER_CHAT_APP_CLUSTER'],
  ssl=True
)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/setname/", methods=['POST'])
def set_name():
    session['name'] = request.form['name']

    return "Succesfull"

@app.route("/pusher/auth/", methods=['POST'])
def pusher_authentication():
    auth = pusher_client.authenticate(
        channel = request.form['channel_name'],
        socket_id = request.form['socket_id'],
        custom_data = {
            'user_id': session['name'],
        }
    )

    return json.dumps(auth)

@app.route("/messages/", methods=['POST'])
def new_message():
    name = request.form['name']
    text = cgi.escape(request.form['text'])
    channel = request.form['channel']

    now = datetime.datetime.now()
    timestamp = time.mktime(now.timetuple()) * 1000
    pusher_client.trigger( "presence-" + channel, 'new_message', {
        'text': text,
        'name': name,
        'time': timestamp
    })

    return "Succesful"

if __name__ == "__main__":
    app.run()