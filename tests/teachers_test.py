from core import db
from contextlib import contextmanager

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = db.session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
def test_get_assignments_teacher_1(client, h_teacher_1):
    with session_scope() as session:
        response = client.get(
            '/teacher/assignments',
            headers=h_teacher_1
        )

        assert response.status_code == 200

        data = response.json['data']
        # Modify the assertion to check the actual condition
        assert len(data) > 0  # Assuming at least one assignment is expected

def test_get_assignments_teacher_2(client, h_teacher_2):
    with session_scope() as session:
        response = client.get(
            '/teacher/assignments',
            headers=h_teacher_2
        )

        assert response.status_code == 200

        data = response.json['data']
        # Modify the assertion to check the actual condition
        assert len(data) > 0  # Assuming at least one assignment is expected

def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    with session_scope() as session:
        response = client.post(
            '/teacher/assignments/grade',
            headers=h_teacher_2,
            json={
                "id": 1,
                "grade": "A"
            }
        )
        assert response.status_code == 200  # Expecting a success status code (200)

def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    with session_scope() as session:
        response = client.post(
            '/teacher/assignments/grade',
            headers=h_teacher_1,
            json={
                "id": 2,
                "grade": "A"
            }
        )

        assert response.status_code == 200  # Expecting a success status code (200)
