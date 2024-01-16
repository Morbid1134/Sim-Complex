from simcomplex import socketio, game

@socketio.on('newCamera')
def handle_new_camera_request(number):
    socketio.emit('currentCamera', game.IP[str(number)])

@socketio.on('taskComplete')
def handle_task_completion(taskName):
    game.guard.taskComplete(taskName)

@socketio.on('pingEnd')
def handle_cameras_off():
    global moving
    if moving >= 3:
        print('something went wrong! pingEnd')
    if moving == 0:
        # send cameras off signal
        print('turn off camera')
        socketio.emit('cameraOff')
    moving += 1

@socketio.on('pingStart')
def handle_cameras_on():
    global moving
    if moving <= 0:
        print('something went wrong! pingStart')

    moving -= 1
    if moving == 0:
        # send cameras on signal
        print('turn on camera')
        socketio.emit('cameraOn')

@socketio.on('terminalInput')
def handle_terminal_input(command):
        game.guard.command(command)