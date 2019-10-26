import jwt
from functools import wraps
from flask import g, request, redirect, url_for, jsonify
from models.User import Users
from bson.objectid import ObjectId

def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    try:
      token = request.headers["Authorization"].replace("Bearer ", "")
      token_info = jwt.decode(token, "secret")
      users = Users.objects(pk= token_info['_id'], tokens__token= token)
      if len(users) == 0: raise Exception("User not authorized")
      request.token = token
      request.user = users[0]
      return f(*args, **kwargs)
    except Exception as e:
      return jsonify({"error": str(e)})
  return decorated_function