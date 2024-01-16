from flask import Blueprint, render_template

tasks = Blueprint('tasks', __name__)

@tasks.route("/enduro")
def enduro():
    return render_template("tasks/enduro.html")

@tasks.route("/2048")
def task_2048():
    return render_template("tasks/2048.html")

@tasks.route("/loading")
def loading():
    return render_template("tasks/loading.html")

@tasks.route("/maze")
def maze():
    return render_template("tasks/maze.html")

@tasks.route("/osu")
def osu():
    return render_template("tasks/osu.html")

@tasks.route("/bin_sorting")
def bin_sorting():
    return render_template("tasks/bin_sorting.html")

@tasks.route("/frogger")
def frogger():
    return render_template("tasks/frogger.html")

@tasks.route("/memory_pattern")
def memory_pattern():
    return render_template("tasks/memory_pattern.html")

@tasks.route("/missle_command")
def missle_command():
    return render_template("tasks/missle_command.html")

@tasks.route("/pong")
def pong():
    return render_template("tasks/pong.html")

@tasks.route("/snake")
def snake():
    return render_template("tasks/snake.html")

@tasks.route("/tetris")
def tetris():
    return render_template("tasks/tetris.html")

@tasks.route("/typing_test")
def typing_test():
    return render_template("tasks/typing_test.html")

@tasks.route("/breakout")
def breakout():
    return render_template("tasks/breakout.html")