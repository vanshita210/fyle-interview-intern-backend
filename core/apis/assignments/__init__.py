from .student import student_assignments_resources
from .teacher import teacher_assignments_resources
from flask import Flask
from core.apis.principal.principal import principal_api

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(principal_api)

    return app
