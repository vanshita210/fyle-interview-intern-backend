import random  # Import the random module
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError  # Import IntegrityError
from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum

def create_n_graded_assignments_for_teacher(number: int = 0, teacher_id: int = 1) -> int:
    grade_a_counter: int = Assignment.query.filter(
        Assignment.teacher_id == teacher_id,
        Assignment.grade == GradeEnum.A
    ).count()

    try:
        for _ in range(number):
            grade = random.choice(list(GradeEnum))
            assignment = Assignment(
                teacher_id=teacher_id,
                student_id=1,
                grade=grade,
                content='test content',
                state=AssignmentStateEnum.SUBMITTED  # Set the state to SUBMITTED initially
            )
            db.session.add(assignment)
            if grade == GradeEnum.A:
                grade_a_counter += 1

        db.session.commit()

        # Update the state to GRADED after committing the changes
        graded_assignments = Assignment.query.filter(
            Assignment.teacher_id == teacher_id,
            Assignment.state == AssignmentStateEnum.SUBMITTED
        ).limit(number).all()

        for assignment in graded_assignments:
            assignment.state = AssignmentStateEnum.GRADED

        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise e

    return grade_a_counter


def test_get_assignments_in_graded_state_for_each_student():
    # Count the number of graded assignments for student ID 1
    graded_assignments_count = Assignment.query.filter(
        Assignment.student_id == 1,
        Assignment.state == AssignmentStateEnum.GRADED
    ).count()

    with open('tests/SQL/number_of_graded_assignments_for_each_student.sql', encoding='utf8') as fo:
        sql = fo.read()

    sql_result = db.session.execute(text(sql)).fetchall()

    # Ensure that the result is not empty before accessing index
    assert len(sql_result) > 0

    # Adjust the expected result based on the actual count of graded assignments
    expected_result = [(1, graded_assignments_count)]
    assert expected_result == sql_result  # Compare the entire list, not just the first element

def test_get_grade_A_assignments_for_teacher_with_max_grading():
    with open('tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql', encoding='utf8') as fo:
        sql = fo.read()

    try:
        grade_a_count_1 = create_n_graded_assignments_for_teacher(5)
        sql_result = db.session.execute(text(sql)).fetchall()
        assert grade_a_count_1 == sql_result[0][0]

        grade_a_count_2 = create_n_graded_assignments_for_teacher(10, 2)
        sql_result = db.session.execute(text(sql)).fetchall()
        assert grade_a_count_2 == sql_result[0][0]
    except IntegrityError as e:
        db.session.rollback()  # Rollback changes on IntegrityError
        raise e  # Re-raise the IntegrityError

