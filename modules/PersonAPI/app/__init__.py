from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api

from udadb import db, Person, PersonSchema # noqa


def register_routes(api, app, root="api"):
    from app.controllers import api as udaconnect_api

    api.add_namespace(udaconnect_api, path=f"/{root}")


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="Persons API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
