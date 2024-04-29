from core.apis.decorators import requires_principal_header
from flask import Blueprint, jsonify, request

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



principal_api = Blueprint('principal_api', __name__)

@principal_api.route('/assignments/grade', methods=['POST'])
@requires_principal_header
def grade_assignment():
    # Get JSON payload from the request
    data = request.get_json()

    # Validate the JSON payload
    if not data or 'id' not in data or 'grade' not in data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    assignment_id = data['id']
    grade = data['grade']

    # Perform additional validation if needed
    if not isinstance(assignment_id, int) or not isinstance(grade, str) or len(grade) != 1:
        return jsonify({'error': 'Invalid assignment ID or grade'}), 400

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

    # Return the graded assignment data in the response
    return jsonify({'data': graded_assignment})