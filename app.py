# Import necessary modules from Flask
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import json
import random
import re

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

# Function to randomly select a task based on predefined probabilities
def get_task():
    tasks = ["enduro", "task_2048", "loading", "maze", "osu"]
    probability = [1, 0, 0, 0, 0]
    chosen_item = random.choices(tasks, weights=probability, k=random.randint(0, 1000))
    return chosen_item

# Initialize a dictionary to store tasks with their completion status
global tasks
tasks = {}
for i in range(5):
    # task = get_task()[0]
    task_list = ["enduro", "task_2048", "loading", "maze", "osu"]
    task = task_list[i]
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

    if request.method == "POST":
        # Update IP dictionary with form values
        for key in IP.keys():
            IP[key] = request.form[key]

        # Save updated IPs to JSON file
        with open(JSON_FILE_PATH, "w") as file:
            json.dump(IP, file)
        
        redirect(url_for('settings'))

    return render_template("settings.html", IP=IP)

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
    return render_template("bonny.html")

@app.route("/freddy")
def freddy():
    return render_template("freddy.html")

@app.route("/chica")
def chica():
    return render_template("chica.html")

@app.route("/boot")
def boot():
    return render_template("boot.html")

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")

@socketio.on('send_message')
def handle_message(message):
    socketio.emit('receive_message', message)

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
        socketio.emit("allTasksCompleted")
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

if __name__ == '__main__':
    initialize_cameras()
    socketio.run(app)