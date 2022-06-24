from crypt import methods
from flask import Blueprint, request, jsonify
from function_jwt import write_token

routes_auth = Blueprint("routes_auth", __name__)

@routes_auth.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    if data.username == "Nelson Hernandez":
        return write_token(data=request.get_json())
    else:
        response = jsonify({"message": "User not found"})
        response.status_code = 404
        return response
