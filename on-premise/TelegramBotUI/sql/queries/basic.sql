SELECT role_id, name, permissions_level 
FROM Role;

SELECT isbn, title, author, year 
FROM Book
WHERE year > 2015;

SELECT person_id, name, phone 
FROM Person
WHERE phone LIKE '123%';

SELECT COUNT(*) AS total_students 
FROM Student;

SELECT room_id, room_type 
FROM Room
WHERE room_type = 'Lab';
