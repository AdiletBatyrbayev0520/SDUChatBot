SELECT student_id, person_id, years_of_study, 
       RANK() OVER (ORDER BY years_of_study DESC) AS rank
FROM Student;

SELECT borrow_date, 
       COUNT(*) OVER (ORDER BY borrow_date) AS cumulative_borrow_count
FROM Person_Book;

SELECT block_id, COUNT(room_id) AS room_count, 
       100.0 * COUNT(room_id) / SUM(COUNT(room_id)) OVER () AS percentage
FROM Room
GROUP BY block_id;
