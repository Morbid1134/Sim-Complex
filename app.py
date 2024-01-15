# Import necessary modules from Flask
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import json
import random
import re
import time

# Cameras IPs
# Example: 10.0.0.198 -> 198
IP = {
    "1": "http://10.0.0.0:8080/video",
    "2": "http://10.0.0.0:8080/video",
    "3": "http://10.0.0.0:8080/video",
    "4": "http://10.0.0.0:8080/video",
    "5": "http://10.0.0.0:8080/video",
    "6": "http://10.0.0.0:8080/video",
    "7": "http://10.0.0.0:8080/video",
    "8": "http://10.0.0.0:8080/video",
    "9": "http://10.0.0.0:8080/video",
}


freddy_min = 50
freddy_max = 50
bonny_min = 50
bonny_max = 50
chica_min = 50
chica_max = 50

# JSON file to store camera IPs
JSON_FILE_PATH = "camera_ips.json"

def initialize_cameras():
    # Load IPs from JSON file if it exists
    try:
        with open(JSON_FILE_PATH, "r") as file:
            data = json.load(file)
            for key in IP.keys():
                if key in data:
                    IP[key] = str(data[key])
    except FileNotFoundError:
        pass

moving = 0
time_to_move = 60


# Create a Flask web application
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initial terminal output containing system information
global terminal_output
terminal_output = ["Linux pi-hole 6.1.21-v7+ #1642 SMP Mon Apr  3 17:20:52 BST 2023 armv7l",
                   "", "The programs included with the Debian GNU/Linux system are free software;",
                   "the exact distribution terms for each program are described in the",
                   "individual files in /usr/share/doc/*/copyright.", "",
                   "Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent",
                   "permitted by applicable law.", "Last login: Sun Dec 17 12:12:06 2023 from 10.0.0.59"]

# Function to randomly select n tasks with no repeats
def get_random_tasks(n):
    ts = ["enduro", "task_2048", "loading", "maze", "osu", "bin_sorting", "frogger", "memory_pattern", "missle_command", "pong", "snake", "tetris", "typing_test", "breakout"]
    
    # Shuffle the tasks to ensure randomness
    random.shuffle(ts)
    
    # Select the first n tasks
    chosen_tasks = ts[:n]
    
    return chosen_tasks

# Initialize a dictionary to store tasks with their completion status
global tasks
global number_of_tasks
tasks = {}
number_of_tasks = 8
for task in get_random_tasks(number_of_tasks):
    tasks[str(task)] = 'Incomplete'

# Initalize no selected tasks
global selected
selected = None

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/settings", methods=["GET", "POST"])
def settings():
    global IP
    global tasks
    global moving
    global number_of_tasks, time_to_move
    global freddy_min, freddy_max, chica_min, chica_max, bonny_min, bonny_max

    if request.method == "POST":
        if "camera-form" in request.form:
            # Update IP dictionary with form values
            for key in IP.keys():
                IP[key] = request.form[key]

            # Save updated IPs to JSON file
            with open(JSON_FILE_PATH, "w") as file:
                json.dump(IP, file)

        elif "task-list" in request.form:
            tasks = {}
            for task in get_random_tasks(number_of_tasks):
                tasks[str(task)] = 'Incomplete'

        elif "reset-game" in request.form:
                number_of_tasks = request.form["number-of-tasks"]
                socketio.emit("allTasksCompleted")
                tasks = {}
                for task in get_random_tasks(int(number_of_tasks)):
                    tasks[str(task)] = 'Incomplete'
            
        elif "movement-time" in request.form:
            # Initialize a dictionary to store tasks with their completion status
            freddy_min = request.form['min_freddy']
            freddy_max = request.form['max_freddy']
            bonny_min = request.form['min_bonny']
            bonny_max = request.form['max_bonny']
            chica_min = request.form['min_chica']
            chica_max = request.form['max_chica']
            time_to_move = request.form['time_to_move']

        redirect(url_for('settings'))
    
    settings_tasks = [i for i in tasks.items()]
    lenTasks = len(settings_tasks)
    return render_template("settings.html", IP=IP, tasks=settings_tasks, lenTasks = lenTasks, min_freddy=freddy_min, max_freddy=freddy_max, min_bonny=bonny_min, max_bonny=bonny_max, min_chica=chica_min, max_chica=chica_max, time_to_move=time_to_move)

# Define a route for the main terminal page
@app.route("/terminal", methods=["GET", "POST"])
def terminal():
    global terminal_output

    # Render the template with updated terminal output
    return render_template("terminal.html", len=len(terminal_output), terminal=terminal_output)

@app.route("/animatronics")
def animatronics():
    return render_template("animatronics.html")

@app.route("/bonny")
def bonny():
    global bonny_min, bonny_max
    return render_template("bonny.html", min=bonny_min, max=bonny_max, moving_time=time_to_move)

@app.route("/freddy")
def freddy():
    global freddy_min, freddy_max
    return render_template("freddy.html", min=freddy_min, max=freddy_max, moving_time=time_to_move)

@app.route("/chica")
def chica():
    global chica_min, chica_max
    return render_template("chica.html", min=chica_min, max=chica_max, moving_time=time_to_move)

@app.route("/boot")
def boot():
    return render_template("boot.html")

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")

@socketio.on('newCamera')
def handle_new_camera_request(number):
    global IP
    socketio.emit('currentCamera', IP[str(number)])

@socketio.on('taskComplete')
def handle_task_completion(taskName):
    global tasks
    tasks[taskName] = "Complete"
    allDone = True
    for task in tasks.items():
        if task[1] != "Complete":
            allDone = False
    if allDone:
        time.sleep(2)
        socketio.emit("allTasksCompleted")
        global moving
        moving = 0
    else:
        socketio.emit("taskCompleted")

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
        global terminal_output
        global tasks
        global selected
        hostname = r"<span class='green'>admin@security:</span><span class='blue'>~ $</span>"
        data = command
        output = str(hostname) + str(data)
        terminal_output.append(output)

        # Command handling based on user input
        if data.lower() == 'task':
            terminal_output.append("Tasks: ")
            for i, task in enumerate(tasks.items()):
                terminal_output.append(f"&emsp;Task {i+1} — {task[1]}")

        elif data.lower() == 'clear':
            # Clear the terminal output
            terminal_output = [""]

        elif data.lower() == 'help':
            # Display help information
            output = ["GNU bash, version 5.1.4(1)-release (arm-unknown-linux-gnueabihf)",
                      "These shell commands are defined internally.  Type `help' to see this list.",
                      "Type `help name' to find out more about the function `name'.", "",
                      "A star (*) next to a name means that the command is disabled.", "",
                      " clear", " help [pattern ...]", " select [-ptr] [NAME]", " task"]
            for item in output:
                terminal_output.append(item)

        # Additional help commands handling
        elif data.lower() == 'help help':
            # Display help for the help command
            output = ["help: help [pattern ...]",
                      "&emsp;Display information about builtin commands.", "",
                      "&emsp;Displays brief summaries of builtin commands.  If PATTERN is",
                      "&emsp;specified, gives detailed help on all commands matching PATTERN,",
                      "&emsp;otherwise the list of help topics is printed.", "",
                      "&emsp;Options:", "", "&emsp;Arguments:",
                      "&emsp;  PATTERN   Pattern specifying a help topic", "", "&emsp;Exit Status:",
                      "&emsp;Returns success unless PATTERN is not found or an invalid option is given."]
            for item in output:
                terminal_output.append(item)

        elif data.lower() == 'help select':
            # Display help for the select command
            output = ["select: select [-prt] [NAME ...]", "", "&emsp;Options:", 
                      "&emsp;  -p        output current selection", "&emsp;  -r        run current selection", 
                      "&emsp;  -t        specify selection of a task",
                      "", "&emsp;Arguments:", "&emsp;  name      Name specifying a known task", "",
                      "&emsp;Exit Status:",
                      "&emsp;Returns success unless an invalid option is supplied or an error occurs."]
            for item in output:
                terminal_output.append(item)

        elif data.lower() == 'help task':
            # Display help for the select command
            output = ["task: task",
                      "&emsp;Display task stack.", "",
                      "&emsp;Display the list of currently remembered tasks.  Tasks",
                      "&emsp;find their way onto the list with the [REDACTED]; you can get",
                      "&emsp;help doing task by—", "", "&emsp;Options:",
                      "", "&emsp;Arguments:", "",
                      "&emsp;Exit Status:",
                      "&emsp;Returns success unless an invalid option is supplied or an error occurs."]
            for item in output:
                terminal_output.append(item)

        elif len(re.split(r' ', data.lower())) == 3 and re.split(r' ', data.lower())[0] == 'select':
            # Display help for the select command
            print(data.lower())
            user_input = re.split(r' ', data.lower())
            if user_input[1] == "-t" or user_input == "task":
                input_task = user_input[2]
                try:
                    input_task = int(input_task)
                    if int(input_task) in range(1, len(tasks)+1):
                        terminal_output.append(f"Task {input_task} is selected")
                        selected = int(input_task)-1
                    else:
                        terminal_output.append(f"-bash: selected -t: {input_task}: task not found")
                except:
                    terminal_output.append(f"-bash: selected -t: {input_task}: task has to be an integer")
            else:
                terminal_output.append(f"-bash: selected: {user_input[2]}: unknown select flag")

        elif len(re.split(r' ', data.lower())) == 2:
            # Display help for the select command
            input_task = re.split(r' ', data.lower())[1]
            if input_task == "-p":
                if selected == None:
                    terminal_output.append(f"No Task Selected")
                else:
                    terminal_output.append(f"Selected Task —> Task {selected+1}")
            elif input_task == "-r":
                items = list(tasks.items())
                task = items[selected]
                task_name = task[0]
                if task_name == None:
                    terminal_output.append(f"-bash: selected -r: no task selected")
                else:
                    terminal_output.append(f"Running Task {selected+1} -> {task_name}.exe")
            else:
                terminal_output.append(f"-bash: {re.split(r' ', data.lower())[0]}: {re.split(r' ', data.lower())[1]}: command not found")


        # Handle unknown commands
        elif data.lower() != '':
            terminal_output.append(f"-bash: {data}: command not found")

        socketio.emit('terminalOutput', terminal_output)

        if len(re.split(r' ', data.lower())) == 2:
            input_task = re.split(r' ', data.lower())[1]
            if input_task == "-r":
                items = list(tasks.items())
                task = items[selected]
                task_name = task[0]
                if task_name != None:
                    socketio.emit('redirect', url_for(f"{task_name}"))



@app.route("/enduro")
def enduro():
    return render_template("enduro.html")

@app.route("/2048")
def task_2048():
    return render_template("2048.html")

@app.route("/loading")
def loading():
    return render_template("loading.html")

@app.route("/maze")
def maze():
    return render_template("maze.html")

@app.route("/osu")
def osu():
    return render_template("osu.html")

@app.route("/bin_sorting")
def bin_sorting():
    return render_template("bin_sorting.html")

@app.route("/frogger")
def frogger():
    return render_template("frogger.html")

@app.route("/memory_pattern")
def memory_pattern():
    return render_template("memory_pattern.html")

@app.route("/missle_command")
def missle_command():
    return render_template("missle_command.html")

@app.route("/pong")
def pong():
    return render_template("pong.html")

@app.route("/snake")
def snake():
    return render_template("snake.html")

@app.route("/tetris")
def tetris():
    return render_template("tetris.html")

@app.route("/typing_test")
def typing_test():
    return render_template("typing_test.html")

@app.route("/breakout")
def breakout():
    return render_template("breakout.html")

if __name__ == '__main__':
    initialize_cameras()
    socketio.run(app, debug=True)