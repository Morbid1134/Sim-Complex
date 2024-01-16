# Import necessary modules from Flask
from flask import Flask
from flask_socketio import SocketIO

# Create a Flask web application
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

from simcomplex.models import Game

game = Game()

from simcomplex.socket import routes
from simcomplex.main.routes import main
from simcomplex.tasks.routes import tasks

app.register_blueprint(main)
app.register_blueprint(tasks)