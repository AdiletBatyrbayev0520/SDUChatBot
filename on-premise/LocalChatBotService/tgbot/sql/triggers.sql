CREATE OR REPLACE FUNCTION validate_year()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.year < 1000 OR NEW.year > EXTRACT(YEAR FROM CURRENT_DATE) THEN
        RAISE EXCEPTION 'Invalid year: % (must be between 1000 and the current year)', NEW.year;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_year_trigger
BEFORE INSERT OR UPDATE ON Book
FOR EACH ROW
EXECUTE FUNCTION validate_year();


UPDATE Book
SET year = 2019
WHERE year = 2004;

UPDATE Book
SET year = 500
WHERE year = 2019;

-----------------------------------------------------------

CREATE OR REPLACE FUNCTION decrease_copies_available()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Book
    SET copies_available = copies_available - 1
    WHERE isbn = NEW.book_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_decrease_copies
AFTER INSERT ON Person_Book
FOR EACH ROW
EXECUTE FUNCTION decrease_copies_available();


INSERT INTO Book (isbn, title, author, subject_code, class_number, cutter, year, publisher, copies_available)
VALUES ('978-3-16-148410-0', 'SQL Basics', 'John Doe', 'CS', 101.50, 'D12', 2020, 'TechBooks', 5);

INSERT INTO Person_Book (person_id, book_id, borrow_date, return_date)
VALUES (1, '978-3-16-148410-0', '2024-11-01', '2024-11-15');

SELECT copies_available FROM Book WHERE isbn = '978-3-16-148410-0';


-----------------------------------------------------------


CREATE OR REPLACE FUNCTION increase_copies_available()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Book
    SET copies_available = copies_available + 1
    WHERE isbn = OLD.book_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_increase_copies
AFTER DELETE ON Person_Book
FOR EACH ROW
EXECUTE FUNCTION increase_copies_available();


DELETE FROM Person_Book
WHERE person_id = 1 AND book_id = '978-3-16-148410-0';

SELECT copies_available FROM Book WHERE isbn = '978-3-16-148410-0';


-----------------------------------------------------------

CREATE OR REPLACE FUNCTION prevent_room_overlaps()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM Person_Room
        WHERE room_id = NEW.room_id
          AND NEW.booking_date < return_date
          AND NEW.return_date > booking_date
    ) THEN
        RAISE EXCEPTION 'Overlapping room booking detected for room_id %', NEW.room_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_overlaps
BEFORE INSERT ON Person_Room
FOR EACH ROW
EXECUTE FUNCTION prevent_room_overlaps();


INSERT INTO Person_Room (person_id, room_id, booking_date, return_date)
VALUES (1, 'Room_101', '2024-11-01 10:00:00', '2024-11-02 12:00:00');

INSERT INTO Person_Room (person_id, room_id, booking_date, return_date)
VALUES (2, 'Room_101', '2024-11-02 11:00:00', '2024-11-03 10:00:00');




-----------------------------------------------------------


CREATE OR REPLACE FUNCTION validate_age()
RETURNS TRIGGER AS $$
BEGIN
    IF AGE(NEW.bday) < INTERVAL '18 years' THEN
        RAISE EXCEPTION 'Person must be at least 18 years old';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_age
BEFORE INSERT OR UPDATE ON Person
FOR EACH ROW
EXECUTE FUNCTION validate_age();


INSERT INTO Person (name, email, phone, bday, role_id)
VALUES ('John Doe', 'john.doe@example.com', '123-456-7890', '2000-01-01', 1);

INSERT INTO Person (name, email, phone, bday, role_id)
VALUES ('Jane Doe', 'jane.doe@example.com', '987-654-3210', '2010-01-01', 2);


-----------------------------------------------------------

CREATE OR REPLACE FUNCTION assign_default_advisor()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.advisor_id IS NULL THEN
        NEW.advisor_id = (SELECT teacher_id FROM Teacher LIMIT 1);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_assign_advisor
BEFORE INSERT ON Student
FOR EACH ROW
EXECUTE FUNCTION assign_default_advisor();

INSERT INTO Student (person_id, speciality_id, years_of_study)
VALUES (1, 'SP_101', 3);

SELECT * FROM Student WHERE person_id = 1;


-----------------------------------------------------------

CREATE OR REPLACE FUNCTION prevent_room_overcapacity()
RETURNS TRIGGER AS $$
DECLARE
    current_count INT;
    room_capacity INT := 10;
BEGIN
    SELECT COUNT(*) INTO current_count
    FROM Person_Room
    WHERE room_id = NEW.room_id;

    IF current_count >= room_capacity THEN
        RAISE EXCEPTION 'Room capacity exceeded for room_id %', NEW.room_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_room_capacity
BEFORE INSERT ON Person_Room
FOR EACH ROW
EXECUTE FUNCTION prevent_room_overcapacity();


DO $$
BEGIN
    FOR i IN 1..10 LOOP
        INSERT INTO Person_Room (person_id, room_id, booking_date, return_date)
        VALUES (i, 'Room_102', '2024-11-01 10:00:00', '2024-11-02 12:00:00');
    END LOOP;
END $$;

INSERT INTO Person_Room (person_id, room_id, booking_date, return_date)
VALUES (11, 'Room_102', '2024-11-03 10:00:00', '2024-11-04 12:00:00');


-----------------------------------------------------------

CREATE OR REPLACE FUNCTION archive_old_groups()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.assignment_date < CURRENT_DATE - INTERVAL '5 years' THEN
        UPDATE Groups
        SET percentage = 0
        WHERE group_id = NEW.group_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_archive_groups
AFTER INSERT OR UPDATE ON Groups
FOR EACH ROW
EXECUTE FUNCTION archive_old_groups();

INSERT INTO Groups (group_id, teacher_id, percentage, assignment_date)
VALUES ('GRP_1', 1, 60, CURRENT_DATE - INTERVAL '1 year');

INSERT INTO Groups (group_id, teacher_id, percentage, assignment_date)
VALUES ('GRP_2', 2, 75, CURRENT_DATE - INTERVAL '6 years');

SELECT * FROM Groups;

-----------------------------------------------------------
-----------------------------------------------------------


