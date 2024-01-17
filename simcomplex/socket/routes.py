from simcomplex import socketio, game

@socketio.on('newCamera')
def handle_new_camera_request(number):
    socketio.emit('currentCamera', game.IP[str(number)])

@socketio.on('taskComplete')
def handle_task_completion(taskName):
    game.guard.taskComplete(taskName)

@socketio.on('isCameraBlurred')
def handle_blur_request():
    if game.check_moving():
        socketio.emit('cameraOff')
    else:
        socketio.emit('cameraOn')

@socketio.on('pingEnd')
def handle_cameras_off(animatronic):
    
    is_moving = game.check_moving()
    if not is_moving:
        print('turn off camera')
        socketio.emit('cameraOff')

    if animatronic == 'chica':
        game.chica.moving = True
    elif animatronic == 'bonny':
        game.bonny.moving = True
    elif animatronic == 'freddy':
        game.freddy.moving = True

@socketio.on('pingStart')
def handle_cameras_on(animatronic):
    if animatronic == 'chica':
        game.chica.moving = False
    elif animatronic == 'bonny':
        game.bonny.moving = False
    elif animatronic == 'freddy':
        game.freddy.moving = False

    is_moving = game.check_moving()
    if not is_moving:
        print('turn on camera')
        socketio.emit('cameraOn')

@socketio.on('terminalInput')
def handle_terminal_input(command):
        game.guard.command(command)
