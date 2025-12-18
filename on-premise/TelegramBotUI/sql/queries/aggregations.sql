SELECT COUNT(*) AS total_books 
FROM Book;

SELECT AVG(years_of_study) AS avg_years_of_study 
FROM Student;

SELECT room_type, COUNT(*) AS room_count 
FROM Room
GROUP BY room_type;

SELECT speciality_id, COUNT(*) AS student_count 
FROM Student
GROUP BY speciality_id;

SELECT MIN(borrow_date) AS earliest_borrow, MAX(borrow_date) AS latest_borrow 
FROM Person_Book;