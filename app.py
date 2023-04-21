from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db = SQLAlchemy(app)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    room = db.Column(db.String(50))
    message = db.Column(db.String(200))

    def __init__(self, username, room, message):
        self.username = username
        self.room = room
        self.message = message


db.create_all()
socketio = SocketIO(app, manage_session=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        username = request.form['username']
        room = request.form['room']
        session['username'] = username
        session['room'] = room
        return redirect(url_for('chat') + f'?username={username}')
    elif session.get('username') is not None:
        return render_template('chat.html', session=session, username=session['username'])
    else:
        return redirect(url_for('index'))

@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg':  session.get('username') + ' has entered the room.',"author":session.get('username')}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    username = session.get('username')
    chat_message = ChatMessage(username, room, message['msg'])
    db.session.add(chat_message)
    db.session.commit()
    emit('message', {'msg': message['msg'],"author":session.get('username')}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)


if __name__ == '__main__':
    socketio.run(app)