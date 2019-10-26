import json
from flask import Blueprint, request, jsonify
from models.User import Users
from middlewares.authentication import login_required

user_page = Blueprint("users", __name__, url_prefix="/users")

@user_page.route("", methods=["POST"])
def handle_users():
  if request.method == "POST":
    data = request.get_json()
    try:
      newUser = Users(**data)
      changed_fields = list(data.keys())
      newUser.save(signal_kwargs={"changed_fields":changed_fields})
      token = newUser.generate_auth_token()
      return jsonify({"user:": json.loads(newUser.to_json()), "token": token})
    except Exception  as e:
      return jsonify({"error": str(e)})

@user_page.route("/login", methods=["POST"])
def login_user():
  if request.method == "POST":
    try:
      data = request.get_json()
      user = Users.find_user_by_credentials(data["mail"], data["password"])
      token = user.generate_auth_token()
      return jsonify({"user:": json.loads(user.to_json()), "token": token})
    except Exception as e:
      return jsonify({"error": str(e)}), 500

@user_page.route("/logout", methods=["POST"])
@login_required
def logout():
  try:
    if request.method == "POST":
      request.user.remove_auth_token(request.token)
      return user.to_json()
  except Exception as e:
    return jsonify({"error": str(e)})

@user_page.route("/logoutall", methods=["POST"])
@login_required
def logoutall():
  try:
    if request.method == "POST":
      request.user.remove_all_auth_token()
      return request.user.to_json()
  except Exception as e:
    return jsonify({"error": str(e)})

@user_page.route("/me", methods=["GET", "PATCH", "DELETE"])
@login_required
def handle_user_by_id():
  try:
    user = request.user
    if len(user) == 0:
      raise Exception("User not found")

    if request.method == "GET":
      return jsonify(json.loads(user.to_json()))
    elif request.method == "PATCH":
      data = request.get_json()
      user.update(**data)
      changed_fields = list(data.keys())
      user.save(signal_kwargs={"changed_fields":changed_fields})
      return jsonify(json.loads(user.to_json()))
    elif request.method == "DELETE":
      user.delete()
      return jsonify(json.loads(user.to_json()))
  except Exception as e:
    return jsonify({"error": str(e)})
