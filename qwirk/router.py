#!/usr/bin/env python3

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
# monkey patching is necessary because this application uses a background
# thread
import eventlet
async_mode = 'eventlet'
eventlet.monkey_patch()

import time
import multiprocessing
from threading import Thread
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
games = {}

#Game bits
# Import multiprocessing
# have a dictionary of game rooms
# start a process for each game
# Message to send out on sockets?

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(10)
        count += 1
        socketio.emit('my response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')


@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    return render_template('index.html')


@socketio.on('join', namespace='/play')
def join_game(message):
    if not 'gameid' in message:
        emit('fault', {'status': 'ERROR', 'message':"Game ID Required"})
        return
    gameid = message['gameid']
    if not gameid in games:
        games[gameid] = {"status":"lobby", "conns":[request.sid]}
    else:
        if games[gameid]['status'] != "lobby":
            emit('fault', {'status': 'ERROR', 'message':"Game has already begun"})
            return
        games[gameid]['conns'].append(request.sid)
    emit('ack',
         {'status':'OK', 'message':'Joined game lobby'})

@socketio.on('start', namespace='/play')
def start_game(message):
    if not 'gameid' in message:
        emit('fault', {'status': 'ERROR', 'message':'Game ID Required'})
        return
    gameid = message['gameid']
    if not gameid in games:
        emit('fault', {'status': 'ERROR', 'message':'Game not found'})
        return
    if games[gameid]['status'] != 'lobby':
        emit('fault', {'status': 'ERROR', 'message':'Game already running'})
        return
    multiprocessing.Process(target=games[gameid][game].run)


@socketio.on('my broadcast event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my room event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True)

