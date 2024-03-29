from flask import Blueprint, request, jsonify
import json
from models.Task import Tasks
from middlewares.authentication import login_required

task_page = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_page.route("", methods=["GET","POST"])
@login_required
def get_tasks():
  if request.method == "GET":
    return Tasks.objects.to_json() 

  if request.method == "POST":
    new_task = Tasks(**request.get_json(), owner=request.user.id)
    try:
      new_task.save()
      return jsonify({"task": json.loads(new_task.to_json())})
    except Exception  as e:
      return jsonify({"error": str(e)})

@task_page.route("/<taskID>", methods=["GET","PATCH", "DELETE"])
@login_required
def handle_task_by_id(taskID):
  try:
    task = Tasks.objects(id=taskID, owner=request.user.pk).as_pymongo()
    if len(task) == 0:
      raise Exception("Task not found")

    if request.method == "GET":
      return task.to_json()

    elif request.method == "PATCH":
      data = request.get_json()
      task.modify(**data)
      return task.to_json()

    elif request.method == "DELETE":
      task.delete()
      return "Deleted task"

  except Exception as e:
    return jsonify({"error": str(e)})