CREATE INDEX idx_person_room_person_id ON Person_Room(person_id);
CREATE INDEX idx_person_room_room_id ON Person_Room(room_id);

CREATE INDEX idx_access_control_role_id ON Access_control(role_id);
CREATE INDEX idx_access_control_room_id ON Access_control(room_id);

CREATE INDEX idx_student_person_id ON Student(person_id);
CREATE INDEX idx_student_speciality_id ON Student(speciality_id);
CREATE INDEX idx_student_advisor_id ON Student(advisor_id);

CREATE INDEX idx_teacher_person_id ON Teacher(person_id);
CREATE INDEX idx_teacher_faculty_id ON Teacher(faculty_id);

CREATE INDEX idx_groups_teacher_id ON Groups(teacher_id);

CREATE INDEX idx_student_group_student_id ON Student_Group(student_id);
CREATE INDEX idx_student_group_group_id ON Student_Group(group_id);

CREATE INDEX idx_course_group_id ON Course(group_id);
CREATE INDEX idx_course_speciality_id ON Course(speciality_id);

CREATE INDEX idx_faculty_block_id ON Faculty(block_id);
CREATE INDEX idx_speciality_faculty_id ON Speciality(faculty_id);
CREATE INDEX idx_room_block_id ON Room(block_id);

CREATE INDEX idx_person_book_person_id ON Person_Book(person_id);
CREATE INDEX idx_person_book_book_id ON Person_Book(book_id);

CREATE INDEX idx_person_room_booking_date ON Person_Room(booking_date);
CREATE INDEX idx_person_room_return_date ON Person_Room(return_date);

CREATE INDEX idx_access_control_expired_date ON Access_control(expired_date);

CREATE INDEX idx_student_years_of_study ON Student(years_of_study);
CREATE INDEX idx_teacher_years_of_work ON Teacher(years_of_work);

CREATE INDEX idx_groups_assignment_date ON Groups(assignment_date);
CREATE INDEX idx_student_group_enrollment_date ON Student_Group(enrollment_date);
