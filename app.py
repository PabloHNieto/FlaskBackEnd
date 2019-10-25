from flask import Flask
from db.db import get_db
from blueprints.user import user_page
from blueprints.task import task_page

app = Flask(__name__)
get_db()

app.register_blueprint(user_page)
app.register_blueprint(task_page)

@app.route("/")
def get_index():
  return "hello"

