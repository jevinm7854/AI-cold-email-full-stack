from time import sleep
from flask import Blueprint, request, jsonify  # type: ignore
import uuid
from ...config.logger import logger
from ..services.emailService import (
    scrape_website,
    extract_jobs,
    query_vectorDB,
    write_email,
)
from ..services.userService import getUserDetails, getChromaDetails

email_bp = Blueprint("email", __name__)


@email_bp.route("/generate", methods=["POST"])
def email():
    logger.info("User signup endpoint called")
    logger.info(f"Received data: {request.json}")
    data = request.get_json()
    submitted_url = data["url"]
    if not submitted_url:
        return jsonify({"error": "URL is missing"}), 400
    id = data["id"]
    getUserInfo = getUserDetails(id)
    if not getUserInfo:
        return jsonify({"error": "User not found"}), 404

    background = getUserInfo["background"]
    name = getUserInfo["name"]
    technicalSkills = getUserInfo["technicalSkills"]
    data_from_website = scrape_website(submitted_url)
    extracted_jobs = extract_jobs(data_from_website)
    if not extracted_jobs:
        return jsonify({"error": "No jobs found"}), 404
    # logger.info(f"Extracted jobs: {extracted_jobs}")
    skills = extracted_jobs[0]["skills"]
    links = query_vectorDB(id, skills)
    email = write_email(extracted_jobs, links, name, background, technicalSkills)
    sleep(5)  # Delay for testing on frontend

    return (
        jsonify(
            {
                "message": "Email sent successfully",
                "email": email,
            }
        ),
        200,
    )


@email_bp.route("/chromaDetails", methods=["POST"])
def chromaDetails():
    logger.info("ChromaDetails endpoint called")
    data = request.get_json()
    id = data["id"]
    res = getChromaDetails(id)
    return jsonify(res), 200
