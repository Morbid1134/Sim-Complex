from flask import render_template, request, redirect, url_for, Blueprint
from simcomplex import socketio, game
import json

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("main/home.html")

@main.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        if "camera-form" in request.form:
            # Update IP dictionary with form values
            for key in game.IP.keys():
                game.IP[key] = request.form[key]

            # Save updated IPs to JSON file
            with open(game.CAMERA_PATH, "w") as file:
                json.dump(game.IP, file)

        elif "task-list" in request.form:
            game.reset_tasks()

        elif "reset-game" in request.form:
            number_of_tasks = request.form["number-of-tasks"]
            socketio.emit("allTasksCompleted")
            game.reset(number_of_tasks)
            
        elif "movement-time" in request.form:
            # Initialize a dictionary to store tasks with their completion status
            game.freddy.min = request.form['min_freddy']
            game.freddy.max = request.form['max_freddy']
            game.bonny.min = request.form['min_bonny']
            game.bonny.max = request.form['max_bonny']
            game.chica.min = request.form['min_chica']
            game.chica.max = request.form['max_chica']
            game.freddy.time_to_move = request.form['time_to_move']
            game.bonny.time_to_move = request.form['time_to_move']
            game.chica.time_to_move = request.form['time_to_move']

        redirect(url_for('main.settings'))
    
    settings_tasks = [i for i in game.guard.tasks.items()]
    lenTasks = len(settings_tasks)
    return render_template("main/settings.html", IP=game.IP, tasks=settings_tasks, lenTasks = lenTasks, freddy=game.freddy, chica=game.chica, bonny=game.bonny)


@main.route("/boot")
def boot():
    return render_template("main/boot.html")

# Define a route for the main terminal page
@main.route("/terminal", methods=["GET", "POST"])
def terminal():
    # Render the template with updated terminal output
    return render_template("main/terminal.html", len=len(game.guard.output), terminal=game.guard.output)

@main.route("/animatronics")
def animatronics():
    return render_template("main/animatronics.html")

@main.route("/bonny")
def bonny():
    return render_template("main/bonny.html", bonny=game.bonny)

@main.route("/freddy")
def freddy():
    return render_template("main/freddy.html", freddy=game.freddy)

@main.route("/chica")
def chica():
    return render_template("main/chica.html", chica=game.chica)
