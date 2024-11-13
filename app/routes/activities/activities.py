from flask import request, jsonify
from . import bp

@bp.route("/", methods=["GET"])
def response():
    return jsonify({"message": "Endpoint called successfully"}), 200

