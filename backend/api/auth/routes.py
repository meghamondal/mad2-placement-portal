"/login"

from flask import Blueprint, request, jsonify
from flask_security.utils import verify_password
from models import *

auth = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth.route("/login", methods=['POST'])

def login():
  data = request.get_json()
  email = data.get("email")
  password = data.get("password")

  if ( not email or not password):
    return jsonify({"message": "Invalid credentials..."}), 400
  
  user = User.query.filter_by(email = email).first_or_404()

  if not user:
    return jsonify({"message" : "User not found"}), 404
  
  if not verify_password(password, user.password):
    return jsonify({"message" : "incorrect password"}), 401
  
  return jsonify({
    "id" : user.u_id,
    "email" : user.email,
    "token" : user.get_auth_token()
  }), 200

