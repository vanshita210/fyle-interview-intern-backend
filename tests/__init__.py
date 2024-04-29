import pytest
from core.server import app as create_app

# Create a separate app instance for testing
@pytest.fixture
def client():
    app = create_app()  # Create the Flask app instance
    with app.test_client() as client:
        yield client


# Import fixtures from conftest.py
from .conftest import client, h_student_1, h_student_2, h_teacher_1, h_teacher_2, h_principal

# Export fixtures to make them available in test files
__all__ = [
    'client',
    'h_student_1',
    'h_student_2',
    'h_teacher_1',
    'h_teacher_2',
    'h_principal',
]
from core.server import app as create_app


# Other fixtures...
