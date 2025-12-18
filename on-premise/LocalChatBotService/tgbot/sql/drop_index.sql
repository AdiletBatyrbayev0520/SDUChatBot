DROP INDEX IF EXISTS idx_person_room_person_id;
DROP INDEX IF EXISTS idx_person_room_room_id;

DROP INDEX IF EXISTS idx_access_control_role_id;
DROP INDEX IF EXISTS idx_access_control_room_id;

DROP INDEX IF EXISTS idx_student_person_id;
DROP INDEX IF EXISTS idx_student_speciality_id;
DROP INDEX IF EXISTS idx_student_advisor_id;

DROP INDEX IF EXISTS idx_teacher_person_id;
DROP INDEX IF EXISTS idx_teacher_faculty_id;

DROP INDEX IF EXISTS idx_groups_teacher_id;

DROP INDEX IF EXISTS idx_student_group_student_id;
DROP INDEX IF EXISTS idx_student_group_group_id;

DROP INDEX IF EXISTS idx_course_group_id;
DROP INDEX IF EXISTS idx_course_speciality_id;

DROP INDEX IF EXISTS idx_faculty_block_id;
DROP INDEX IF EXISTS idx_speciality_faculty_id;
DROP INDEX IF EXISTS idx_room_block_id;

DROP INDEX IF EXISTS idx_person_book_person_id;
DROP INDEX IF EXISTS idx_person_book_book_id;

DROP INDEX IF EXISTS idx_person_room_booking_date;
DROP INDEX IF EXISTS idx_person_room_return_date;

DROP INDEX IF EXISTS idx_access_control_expired_date;

DROP INDEX IF EXISTS idx_student_years_of_study;
DROP INDEX IF EXISTS idx_teacher_years_of_work;

DROP INDEX IF EXISTS idx_groups_assignment_date;
DROP INDEX IF EXISTS idx_student_group_enrollment_date;
