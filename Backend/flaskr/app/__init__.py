from flask import Flask
import logging
from ..config.dbConfig import Config
from ..config.dbSetup import mysql
from ..config.dbSetup import init_db
from .routes import init_app_routes


def create_app():

    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)  # Change to logging.DEBUG for more details

    app.config.from_object(Config)
    init_db(app)
    init_app_routes(app)

    @app.route("/")
    def hello():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM coldEmail.users")
        result = cur.fetchall()
        return str(result)

    return app
