SELECT COUNT(*) AS grade_a_count
FROM assignments
WHERE teacher_id = (
    SELECT teacher_id
    FROM (
        SELECT teacher_id, COUNT(*) AS graded_count
        FROM assignments
        WHERE state = 'GRADED'
        GROUP BY teacher_id
        ORDER BY graded_count DESC
        LIMIT 1
    ) AS max_graded_teacher
)
AND grade = 'A';
