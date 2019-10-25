from flask import Blueprint, request, jsonify
from models.Task import Tasks

task_page = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_page.route("", methods=["GET","POST"])
def get_tasks():
  if request.method == "GET":
    return Tasks.objects.to_json() 

  if request.method == "POST":
    new_task = Tasks(**request.get_json())
    try:
      new_task.save()
      return new_task.to_json()
    except Exception  as e:
      return jsonify({"error": str(e)})

@task_page.route("/<taskID>", methods=["GET","PATCH", "DELETE"])
def handle_task_by_id(taskID):
  try:
    task = Tasks.objects(id=taskID).as_pymongo()
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