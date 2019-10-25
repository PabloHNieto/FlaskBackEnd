from mongoengine import connect

def get_db():
  connect("task-manager-api")