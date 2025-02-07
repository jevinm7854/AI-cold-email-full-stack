from flask import Blueprint, request, jsonify
import uuid
from ...config.logger import logger
from ..services.userService import createUserDB, createUserChroma

users_bp = Blueprint("users", __name__)


@users_bp.route("/signup", methods=["POST"])
def users():
    logger.info("User signup endpoint called")

    data = request.get_json()

    logger.info(f"Received data: {data}")

    try:
        name = data.get("name")
        email = data.get("email")
        background = data.get("background")
        id = uuid.uuid4()

        # Create user in the database
        responseDB = createUserDB(name, email, id, background)
        if "error" in responseDB:
            logger.error(f"Error creating user in DB: {responseDB['error']}")
            return jsonify({"error": "Failed to create user in database"}), 500

        # Create user in Chroma
        responseChroma = createUserChroma(id, data)
        if "error" in responseChroma:
            logger.error(f"Error creating user in Chroma: {responseChroma['error']}")
            return jsonify({"error": "Failed to create user in ChromaDB"}), 500

        # If both responses are successful, return 201
        logger.info("User created successfully in both DB and Chroma")
        return jsonify({"id": id, "message": "User created successfully"}), 201

    except Exception as e:
        logger.error(f"Error during user signup: {e}", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500
