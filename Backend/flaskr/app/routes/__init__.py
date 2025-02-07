from flask import Blueprint
from . import users
from . import email


def init_app_routes(app):

    app.register_blueprint(users.users_bp, url_prefix="/api/users")
    app.register_blueprint(email.email_bp, url_prefix="/api/email")
