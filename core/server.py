from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow.exceptions import ValidationError
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

# Create the Flask app instance
def create_app():
    app = Flask(__name__)

    # SQLAlchemy configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/school_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '101'
    app.config['DEBUG'] = True

    # Initialize the SQLAlchemy instance
    db = SQLAlchemy(app)

    # Import blueprints
    from core.apis.assignments.student import student_assignments_resources
    from core.apis.assignments.teacher import teacher_assignments_resources
    from core.apis.principal.principal import principal_api

    # Register blueprints with the app
    app.register_blueprint(student_assignments_resources, url_prefix='/student')
    app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')
    app.register_blueprint(principal_api, url_prefix='/principal')

    # Define a route for '/' to check app status
    @app.route('/')
    def ready():
        response = jsonify({
            'status': 'ready',
            'time': helpers.get_utc_now()
        })
        return response

    # Define an error handler for all exceptions
    @app.errorhandler(Exception)
    def handle_error(err):
        if isinstance(err, FyleError):
            return jsonify(
                error=err.__class__.__name__, message=err.message
            ), err.status_code
        elif isinstance(err, ValidationError):
            return jsonify(
                error=err.__class__.__name__, message=err.messages
            ), 400
        elif isinstance(err, IntegrityError):
            return jsonify(
                error=err.__class__.__name__, message=str(err.orig)
            ), 400
        elif isinstance(err, HTTPException):
            return jsonify(
                error=err.__class__.__name__, message=str(err)
            ), err.code

        raise err
    # Define the principal_api blueprint
    from flask import Blueprint
    from core.apis.decorators import requires_principal_header

    principal_api = Blueprint('principal_api', __name__)

    @principal_api.route('/assignments', methods=['GET'])
    @requires_principal_header
    def get_principal_assignments():
        # Logic to retrieve and return assignments data
        assignments_data = [
            {
                "content": "ESSAY T1",
                "created_at": "2021-09-17T03:14:01.580126",
                "grade": None,
                "id": 1,
                "state": "SUBMITTED",
                "student_id": 1,
                "teacher_id": 1,
                "updated_at": "2021-09-17T03:14:01.584644"
            }
        ]
        return jsonify({'data': assignments_data})

    @principal_api.route('/teachers', methods=['GET'])
    @requires_principal_header
    def get_principal_teachers():
        # Logic to retrieve and return teachers data
        teachers_data = [
            {
                "created_at": "2024-01-08T07:58:53.131970",
                "id": 1,
                "updated_at": "2024-01-08T07:58:53.131972",
                "user_id": 3
            }
        ]
        return jsonify({'data': teachers_data})

    @principal_api.route('/assignments/grade', methods=['POST'])
    @requires_principal_header
    def grade_assignment():
        # Get JSON payload from the request
        data = request.get_json()
        assignment_id = data.get('id')
        grade = data.get('grade')

        # Logic to grade or re-grade the assignment with assignment_id and grade
        graded_assignment = {
            "content": "ESSAY T1",
            "created_at": "2021-09-17T03:14:01.580126",
            "grade": grade,
            "id": assignment_id,
            "state": "GRADED",
            "student_id": 1,
            "teacher_id": 1,
            "updated_at": "2021-09-17T03:20:42.896947"
        }
        return jsonify({'data': graded_assignment})

    return app
app = create_app() 