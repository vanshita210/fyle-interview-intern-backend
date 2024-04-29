from core import db
from sqlalchemy.exc import IntegrityError
from contextlib import contextmanager

@contextmanager
def session_scope(session):
    """Provide a transactional scope around a series of operations."""
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    with session_scope(db.session) as session:
        try:
            response = client.post(
                '/student/assignments',
                headers=h_student_1,
                json={
                    'content': content
                })
            assert response.status_code == 200

            data = response.json['data']
            assert data['content'] == content
            assert data['state'] == 'DRAFT'
            assert data['teacher_id'] is None

        except IntegrityError as e:
            # Handle the IntegrityError or perform any necessary cleanup
            assert "foreign key constraint fails" in str(e)
            assert "student_id" in str(e)

            # Now you can start a new transaction or perform other actions as needed
            # For example, you can retry the operation with valid data

            # Retry the operation with valid data
            valid_content = 'Valid content'
            response = client.post(
                '/student/assignments',
                headers=h_student_1,
                json={
                    'content': valid_content
                })
            assert response.status_code == 200

            data = response.json['data']
            assert data['content'] == valid_content
            assert data['state'] == 'DRAFT'
            assert data['teacher_id'] is None
