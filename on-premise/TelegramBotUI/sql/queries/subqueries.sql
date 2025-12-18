SELECT title, author 
FROM Book
WHERE isbn = (
    SELECT book_id 
    FROM Person_Book
    GROUP BY book_id
    ORDER BY COUNT(*) DESC
    LIMIT 1
);

SELECT t.teacher_id, pt.name 
FROM Teacher t
JOIN Person pt ON t.person_id = pt.person_id
WHERE t.faculty_id = (
    SELECT faculty_id 
    FROM Student s
    JOIN Speciality sp ON s.speciality_id = sp.speciality_id
    GROUP BY sp.faculty_id
    ORDER BY COUNT(s.student_id) DESC
    LIMIT 1
);

SELECT p.name 
FROM Person p
WHERE p.person_id IN (
    SELECT person_id 
    FROM Person_Book
    GROUP BY person_id
    HAVING COUNT(book_id) > 3
);

SELECT b.name 
FROM Block b
WHERE b.block_id NOT IN (
    SELECT block_id 
    FROM Room r
    JOIN Person_Room pr ON r.room_id = pr.room_id
);

SELECT name 
FROM Speciality
WHERE speciality_id NOT IN (
    SELECT speciality_id 
    FROM Course
);
