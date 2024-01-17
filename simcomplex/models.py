from flask import url_for
import json, random, re
from simcomplex import socketio
import time

class Game():

    def __init__(self):
        self.IP = dict([(str(key), "http://10.0.0.0:8080/video") for key in range(1,10)])
        self.CAMERA_PATH = "camera_ips.json"
        self.initialize_cameras()

        self.isRunning = False
    
        self.freddy = Animatronic()
        self.chica = Animatronic()
        self.bonny = Animatronic()
        self.guard = Terminal()
        
        self.characterMoving = self.check_moving()

    def initialize_cameras(self):
        try:
            with open(self.CAMERA_PATH, "r") as file:
                data = json.load(file)
                for key in self.IP.keys():
                    if key in data:
                        self.IP[key] = str(data[key])
        except FileNotFoundError:
            with open(self.CAMERA_PATH, "w") as file:
                json.dump(self.IP, file)
            
    def check_moving(self):
        if self.bonny.moving or self.freddy.moving or self.chica.moving:
            return True
    
    def reset(self, number_of_tasks):
        self.guard = None
        self.guard = Terminal(int(number_of_tasks))

        
    def reset_tasks(self):
        number_of_tasks = self.guard.number_of_tasks
        self.guard.tasks = self.guard.get_random_tasks(number_of_tasks)


class Animatronic():
    def __init__(self):
        self.min = 50
        self.max = 50
        self.time_to_move = 60
        self.moving = False

class Terminal():
    def __init__(self, number_of_tasks=9):
        
        # Initial terminal output containing system information
        self.output = ["Linux pi-hole 6.1.21-v7+ #1642 SMP Mon Apr  3 17:20:52 BST 2023 armv7l",
                        "", "The programs included with the Debian GNU/Linux system are free software;",
                        "the exact distribution terms for each program are described in the",
                        "individual files in /usr/share/doc/*/copyright.", "",
                        "Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent",
                        "permitted by applicable law.", "Last login: Sun Dec 17 12:12:06 2023 from 10.0.0.59"]
        task_list=["enduro", "task_2048", "loading", "maze", "osu", "bin_sorting", "frogger", "memory_pattern", "missle_command", "pong", "snake", "tetris", "typing_test", "breakout"]
        self.task_list = dict([(task, True) for task in task_list])
        self.number_of_tasks = number_of_tasks
        self.tasks = Terminal.get_random_tasks(self, self.number_of_tasks)
        self.selected = None
    
        # Function to randomly select n tasks with no repeats
    def get_random_tasks(self, n):
        tasks = [task for task in self.task_list if self.task_list[task] == True]
        print(tasks)
        
        # Shuffle the tasks to ensure randomness
        random.shuffle(tasks)
        
        # Select the first n tasks
        chosen_tasks = tasks[:n]
        
        tasks = {}
        for task in chosen_tasks:
            tasks[str(task)] = 'Incomplete'

        return tasks

    def command(self, command):
        hostname = r"<span class='green'>admin@security:</span><span class='blue'>~ $</span>"
        data = command
        output = str(hostname) + str(data)
        self.output.append(output)

        # Command handling based on user input
        if data.lower() == 'task':
            self.output.append("Tasks: ")
            for i, task in enumerate(self.tasks.items()):
                self.output.append(f"&emsp;Task {i + 1} — {task[1]}")

        elif data.lower() == 'clear':
            # Clear the terminal output
            self.output = [""]

        elif data.lower() == 'help':
            # Display help information
            output = ["GNU bash, version 5.1.4(1)-release (arm-unknown-linux-gnueabihf)",
                      "These shell commands are defined internally.  Type `help' to see this list.",
                      "Type `help name' to find out more about the function `name'.", "",
                      "A star (*) next to a name means that the command is disabled.", "",
                      " clear", " help [pattern ...]", " select [-ptr] [NAME]", " task"]
            for item in output:
                self.output.append(item)

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
                self.output.append(item)

      
        elif data.lower() == 'help select':
            # Display help for the select command
            output = ["select: select [-prt] [NAME ...]", "", "&emsp;Options:", 
                      "&emsp;  -p        output current selection", "&emsp;  -r        run current selection", 
                      "&emsp;  -t        specify selection of a task",
                      "", "&emsp;Arguments:", "&emsp;  name      Name specifying a known task", "",
                      "&emsp;Exit Status:",
                      "&emsp;Returns success unless an invalid option is supplied or an error occurs."]
            for item in output:
                self.output.append(item)

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
                self.output.append(item)

        elif len(re.split(r' ', data.lower())) == 3 and re.split(r' ', data.lower())[0] == 'select':
            # Display help for the select command
            print(data.lower())
            user_input = re.split(r' ', data.lower())
            if user_input[1] == "-t" or user_input == "task":
                input_task = user_input[2]
                try:
                    input_task = int(input_task)
                    if int(input_task) in range(1, len(self.tasks)+1):
                        self.output.append(f"Task {input_task} is selected")
                        self.selected = int(input_task)-1
                    else:
                        self.output.append(f"-bash: selected -t: {input_task}: task not found")
                except:
                    self.output.append(f"-bash: selected -t: {input_task}: task has to be an integer")
            else:
                self.output.append(f"-bash: selected: {user_input[2]}: unknown select flag")

        elif len(re.split(r' ', data.lower())) == 2:
            # Display help for the select command
            input_task = re.split(r' ', data.lower())[1]
            if input_task == "-p":
                if self.selected == None:
                    self.output.append(f"No Task Selected")
                else:
                    self.output.append(f"Selected Task —> Task {self.selected+1}")
            elif input_task == "-r":
                items = list(self.tasks.items())
                task = items[self.selected]
                task_name = task[0]
                if task_name == None:
                    self.output.append(f"-bash: selected -r: no task selected")
                else:
                    self.output.append(f"Running Task {self.selected+1} -> {task_name}.exe")
            else:
                self.output.append(f"-bash: {re.split(r' ', data.lower())[0]}: {re.split(r' ', data.lower())[1]}: command not found")


        # Handle unknown commands
        elif data.lower() != '':
            self.output.append(f"-bash: {data}: command not found")

        socketio.emit('terminalOutput', self.output)

        if len(re.split(r' ', data.lower())) == 2:
            input_task = re.split(r' ', data.lower())[1]
            if input_task == "-r":
                items = list(self.tasks.items())
                task = items[self.selected]
                task_name = task[0]
                if task_name != None:
                    socketio.emit('redirect', url_for(f"tasks.{task_name}"))
    
    def taskComplete(self, task_name):
        self.tasks[task_name] = "Complete"
        allDone = True
        for task in self.tasks.items():
            if task[1] != "Complete":
                allDone = False
        if allDone:
            time.sleep(2)
            socketio.emit("allTasksCompleted")
        else:
            socketio.emit("taskCompleted")