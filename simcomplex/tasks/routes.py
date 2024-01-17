from flask import Blueprint, render_template
from simcomplex import game

tasks = Blueprint('tasks', __name__)

for task in [task[0] for task in game.guard.task_list.items()]:
    route_name = f"/{task}"

    # Use route as a function and set the endpoint explicitly
    tasks.route(route_name, endpoint=f"{task}")(lambda task_name=task: render_template(f"tasks/{task_name}.html"))