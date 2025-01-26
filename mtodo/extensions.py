from flask_login import current_user
from flask_socketio import SocketIO, emit, join_room, leave_room, send

socketio = SocketIO()


@socketio.on("join")
def on_join(data):
    if current_user:
        room = str(current_user.id)
        join_room(room)


@socketio.on("leave")
def on_leave(data):
    if current_user:
        room = str(current_user.id)
        leave_room(room)
