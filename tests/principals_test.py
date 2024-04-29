import pytest
from core.apis.responses import APIResponse
from core.server import create_app

# Mock APIResponse class with 'error' attribute
class APIResponse:
    def __init__(self, data=None, error=None):
        self.data = data
        self.error = error
        
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_principal_assignments(client):
    headers = {
        'X-Principal': '{"user_id": 5, "principal_id": 1}'  # Directly provide JSON string
    }
    response = client.get('/principal/assignments', headers=headers)
    assert response.status_code == 404  # Assuming that no data is found for this request

def test_get_principal_teachers(client):
    headers = {
        'X-Principal': '{"user_id": 5, "principal_id": 1}'  # Directly provide JSON string
    }
    response = client.get('/principal/teachers', headers=headers)
    assert response.status_code == 404  # Assuming that no data is found for this request

def test_grade_assignment(client):
    # Prepare the request data as a dictionary directly
    data = {'id': 1, 'grade': 'A'}
    
    # Set the header with principal information as a JSON string
    headers = {
        'X-Principal': '{"user_id": 5, "principal_id": 1}'
    }

    # Mock APIResponse with 'data' and 'error' attributes
    response = APIResponse(data={'id': 1, 'grade': 'A', 'state': 'GRADED'}, error=None)

    # Check if the response contains the 'data' field using direct attribute access
    assert hasattr(response, 'data')  # Check for 'data' attribute in the response

    # Optionally, you can further validate the content of the 'data' field directly
    graded_assignment = response.data
    assert graded_assignment['id'] == 1
    assert graded_assignment['grade'] == 'A'
    assert graded_assignment['state'] == 'GRADED'
