from time import sleep
from flask import Blueprint, request, jsonify  # type: ignore
import uuid
from ...config.logger import logger
from ..services.emailService import scrape_website, extract_jobs

email_bp = Blueprint("email", __name__)


@email_bp.route("/generate", methods=["POST"])
def email():
    logger.info("User signup endpoint called")
    logger.info(f"Received data: {request.json}")
    data = request.get_json()
    submitted_url = data["url"]
    data_from_website = scrape_website(submitted_url)
    extracted_jobs = extract_jobs(data_from_website)
    sleep(15)  # Delay for testing on frontend
    return (
        jsonify(
            {
                "message": "Email sent successfully",
                "email": f"This is test email from Flask. Say hi!. This is email for {submitted_url} ",
                "extracted_job": extracted_jobs,
            }
        ),
        200,
    )
