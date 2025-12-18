SELECT p.name, b.title, b.author, pb.borrow_date
FROM Person p
INNER JOIN Person_Book pb ON p.person_id = pb.person_id
INNER JOIN Book b ON pb.book_id = b.isbn;

SELECT s.student_id, p.name AS student_name, g.group_id
FROM Student s
LEFT JOIN Person p ON s.person_id = p.person_id
LEFT JOIN Student_Group sg ON s.student_id = sg.student_id
LEFT JOIN Groups g ON sg.group_id = g.group_id;

SELECT g.group_id, p.name AS student_name, sg.student_id
FROM Groups g
RIGHT JOIN Student_Group sg ON g.group_id = sg.group_id
RIGHT JOIN Student s ON sg.student_id = s.student_id
RIGHT JOIN Person p ON s.person_id = p.person_id;

SELECT f.name AS faculty_name, t.teacher_id, pt.name AS teacher_name
FROM Faculty f
FULL OUTER JOIN Teacher t ON f.faculty_id = t.faculty_id
FULL OUTER JOIN Person pt ON t.person_id = pt.person_id;

SELECT b.title, r.room_id, r.room_type
FROM Book b
CROSS JOIN Room r;

SELECT c.course_id, c.name AS course_name, sp.name AS speciality_name
FROM Course c
INNER JOIN Speciality sp ON c.speciality_id = sp.speciality_id
WHERE sp.speciality_id = 'SP_1';

SELECT s.student_id, sp.name AS student_name, t.teacher_id, ta.name AS advisor_name
FROM Student s
LEFT JOIN Teacher t ON s.advisor_id = t.teacher_id
LEFT JOIN Person sp ON s.person_id = sp.person_id
LEFT JOIN Person ta ON t.person_id = ta.person_id;

SELECT r.room_id, r.room_type, ac.role_id
FROM Room r
RIGHT JOIN Access_control ac ON r.room_id = ac.room_id;

SELECT sg.student_id, p.name AS student_name, sg.grade, g.group_id
FROM Student_Group sg
FULL OUTER JOIN Student s ON sg.student_id = s.student_id
FULL OUTER JOIN Person p ON s.person_id = p.person_id
FULL OUTER JOIN Groups g ON sg.group_id = g.group_id;

SELECT b.name AS block_name, r.room_id, r.room_type
FROM Block b
CROSS JOIN Room r;