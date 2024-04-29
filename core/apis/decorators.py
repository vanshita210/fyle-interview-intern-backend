import json
from flask import request
from core.libs import assertions  # Assuming this is correctly imported
from core.apis.responses import APIResponse  # Assuming this is correctly imported
from functools import wraps

def requires_principal_header(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        principal_header = request.headers.get('X-Principal')
        if not principal_header:
            return APIResponse.error(message='Principal header missing', status_code=400)

        try:
            principal_data = json.loads(principal_header)
        except json.JSONDecodeError:
            return APIResponse.error(message='Invalid JSON in principal header', status_code=400)

        # Check if the required keys are present in the principal data
        required_keys = ['user_id', 'student_id', 'teacher_id', 'principal_id']
        if not all(key in principal_data for key in required_keys):
            return APIResponse.error(message='Principal header missing required keys', status_code=400)

        return func(*args, **kwargs)

    return wrapper

class AuthPrincipal:
    def __init__(self, user_id, student_id=None, teacher_id=None, principal_id=None):
        self.user_id = user_id
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.principal_id = principal_id

def accept_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        incoming_payload = request.json
        return func(incoming_payload, *args, **kwargs)
    return wrapper

def authenticate_principal(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        p_str = request.headers.get('X-Principal')
        assertions.assert_auth(p_str is not None, 'principal not found')  # Placeholder, define or import assert_auth
        p_dict = json.loads(p_str)
        p = AuthPrincipal(
            user_id=p_dict['user_id'],
            student_id=p_dict.get('student_id'),
            teacher_id=p_dict.get('teacher_id'),
            principal_id=p_dict.get('principal_id')
        )

        if request.path.startswith('/student'):
            assertions.assert_true(p.student_id is not None, 'requester should be a student')  # Placeholder
        elif request.path.startswith('/teacher'):
            assertions.assert_true(p.teacher_id is not None, 'requester should be a teacher')  # Placeholder
        elif request.path.startswith('/principal'):
            assertions.assert_true(p.principal_id is not None, 'requester should be a principal')  # Placeholder
        else:
            assertions.assert_found(None, 'No such api')  # Placeholder

        return func(p, *args, **kwargs)
    return wrapper
