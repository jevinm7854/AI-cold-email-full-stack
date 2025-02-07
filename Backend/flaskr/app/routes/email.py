from time import sleep
from flask import Blueprint, request, jsonify
import uuid
from ...config.logger import logger

email_bp = Blueprint("email", __name__)


@email_bp.route("/generate", methods=["POST"])
def email():
    logger.info("User signup endpoint called")
    logger.info(f"Received data: {request.json}")
    data = request.get_json()
    submitted_url = data["url"]
    sleep(15)  # Delay for testing on frontend
    return (
        jsonify(
            {
                "message": "Email sent successfully",
                "email": f"This is test email from Flask. Say hi!. This is email for {submitted_url} ",
            }
        ),
        200,
    )
