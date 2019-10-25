from flask import Blueprint, request, jsonify
from models.User import Users
import json

user_page = Blueprint("users", __name__, url_prefix="/users")

# @user_page.route("/", defaults={"page": "index"})
@user_page.route("", methods=["GET", "POST"])
def handle_users():
  if request.method == "GET":
    return Users.objects.to_json()
  
  if request.method == "POST":
    data = request.get_json()
    try:
      newUser = Users(**data)
      changed_fields = list(data.keys())
      newUser.save(signal_kwargs={"changed_fields":changed_fields})
      return newUser.to_json()
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

@user_page.route("/<userID>", methods=["GET", "PATCH", "DELETE"])
def handle_user_by_id(userID):
  
  try:
    user = Users.objects(id=userID).as_pymongo()
    if len(user) == 0:
      raise Exception("User not found")

    if request.method == "GET":
      return user.to_json()

    elif request.method == "PATCH":
      data = request.get_json()
      user.modify(**data)
      return user.to_json()

    elif request.method == "DELETE":
      user.delete()
      return "Deleted user"

  except Exception as e:
    return jsonify({"error": str(e)})
