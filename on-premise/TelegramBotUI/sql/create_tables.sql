CREATE TABLE Role(
    role_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    permissions_level VARCHAR(20) NOT NULL
);

CREATE TABLE Person (
    person_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    bday DATE,
    role_id INT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES Role(role_id)
);

CREATE TABLE Book(
    isbn VARCHAR(13) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100),
    subject_code CHAR(2) NOT NULL,
    class_number NUMERIC(5, 2) NOT NULL,
    cutter VARCHAR(10),
    year INT NOT NULL,
    publisher VARCHAR(100),
    copies_available INT DEFAULT 1 CHECK (copies_available >= 0)
);

CREATE TABLE Person_Book(
    person_id INT NOT NULL,
    book_id VARCHAR(13) NOT NULL,
    borrow_date DATE,
    return_date DATE,
    PRIMARY KEY (person_id, book_id),
    FOREIGN KEY (person_id) REFERENCES Person(person_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES Book(isbn) ON DELETE CASCADE
);

CREATE TABLE Block(
    block_id VARCHAR(1) PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE Room(
    room_id VARCHAR(10) PRIMARY KEY,
    block_id VARCHAR(1) NOT NULL,
    room_type VARCHAR(50) NOT NULL,
    FOREIGN KEY (block_id) REFERENCES Block(block_id)
);

CREATE TABLE Person_Room(
    person_id INT NOT NULL,
    room_id VARCHAR(10) NOT NULL,
    booking_date TIMESTAMP NOT NULL,
    return_date TIMESTAMP NOT NULL CHECK (return_date >= booking_date),
    PRIMARY KEY (person_id, room_id),
    FOREIGN KEY (person_id) REFERENCES Person(person_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES Room(room_id) ON DELETE CASCADE
);

CREATE TABLE Access_control(
    role_id INT NOT NULL,
    room_id VARCHAR(10) NOT NULL,
    expired_date DATE DEFAULT CURRENT_DATE + INTERVAL '5 months',
    PRIMARY KEY (role_id, room_id),
    FOREIGN KEY (role_id) REFERENCES Role(role_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES Room(room_id) ON DELETE CASCADE
);

CREATE TABLE Faculty(
    faculty_id SERIAL PRIMARY KEY,
    block_id VARCHAR(1),
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (block_id) REFERENCES Block(block_id)
);

CREATE TABLE Speciality(
    speciality_id VARCHAR(10) PRIMARY KEY,
    faculty_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    program_details TEXT,
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id)
);

CREATE TABLE Teacher(
    teacher_id SERIAL PRIMARY KEY,
    person_id INT NOT NULL,
    faculty_id INT NOT NULL,
    car_plate_number VARCHAR(15),
    years_of_work INT,
    FOREIGN KEY (person_id) REFERENCES Person(person_id),
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id)
);

CREATE TABLE Student(
    student_id SERIAL PRIMARY KEY,
    person_id INT NOT NULL,
    speciality_id VARCHAR(10) NOT NULL,
    advisor_id INT,
    years_of_study INT CHECK (years_of_study >= 1),
    FOREIGN KEY (person_id) REFERENCES Person(person_id),
    FOREIGN KEY (speciality_id) REFERENCES Speciality(speciality_id),
    FOREIGN KEY (advisor_id) REFERENCES Teacher(teacher_id)
);

CREATE TABLE Groups(
    group_id VARCHAR(15) PRIMARY KEY,
    teacher_id INT NOT NULL,
    percentage INT DEFAULT 60,
    assignment_date DATE NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id)
);

CREATE TABLE Student_Group(
    student_id INT NOT NULL,
    group_id VARCHAR(15) NOT NULL,
    enrollment_date DATE NOT NULL,
    grade VARCHAR(2),
    PRIMARY KEY (student_id, group_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (group_id) REFERENCES Groups(group_id)
);

CREATE TABLE Course(
    course_id VARCHAR(10) NOT NULL,
    group_id VARCHAR(15),
    speciality_id VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    FOREIGN KEY (group_id) REFERENCES Groups(group_id),
    FOREIGN KEY (speciality_id) REFERENCES Speciality(speciality_id)
);
