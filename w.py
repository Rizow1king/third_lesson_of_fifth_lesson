import psycopg2
from pprint import pprint

db = psycopg2.connect(
    database='test',
    user='postgres',
    host='localhost',
    password='1'
)
cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS school(
        school_id SERIAL PRIMARY KEY,
        school_name VARCHAR(150),
        address VARCHAR(50),
        phone_number CHAR(20),
        public_school BOOL DEFAULT True
    );

    CREATE TABLE IF NOT EXISTS teacher(
        teacher_id SERIAL PRIMARY KEY,
        first_name VARCHAR(20),
        last_name VARCHAR(30),
        email VARCHAR(50),
        phone_number CHAR(20),
        school_id INTEGER REFERENCES school(school_id)
    );

    CREATE TABLE IF NOT EXISTS student(
        student_id SERIAL PRIMARY KEY,
        first_name VARCHAR(20),
        last_name VARCHAR(30),
        date_of_birth DATE,
        gender VARCHAR(10),
        school_id INTEGER REFERENCES school(school_id)
    );

    CREATE TABLE IF NOT EXISTS class(
        class_id SERIAL PRIMARY KEY,
        name VARCHAR(20),
        teacher_id INTEGER REFERENCES teacher(teacher_id),
        school_id INTEGER REFERENCES school(school_id)
    );

    CREATE TABLE IF NOT EXISTS subject(
        subject_id SERIAL PRIMARY KEY,
        name VARCHAR(20),
        class_id INTEGER REFERENCES class(class_id),
        teacher_id INTEGER REFERENCES teacher(teacher_id)
    );

    CREATE TABLE IF NOT EXISTS enrollment(
        enrolment_id SERIAL PRIMARY KEY,
        student_id INTEGER REFERENCES student(student_id),
        class_id INTEGER REFERENCES class(class_id),
        enrollment_date DATE DEFAULT CURRENT_DATE
    );

    CREATE TABLE IF NOT EXISTS grade(
        id SERIAL PRIMARY KEY,
        student_id INTEGER REFERENCES student(student_id),
        subject_id INTEGER REFERENCES subject(subject_id),
        grade INTEGER,
        added DATE DEFAULT CURRENT_DATE
    );

    CREATE TABLE IF NOT EXISTS attendance(
        attendance_id SERIAL PRIMARY KEY,
        student_id INTEGER REFERENCES student(student_id),
        class_id INTEGER REFERENCES class(class_id),
        date DATE DEFAULT CURRENT_DATE
    );
''')

cursor.execute('''
    INSERT INTO school(school_name, address, phone_number, public_school) VALUES
    ('presedent school', 'Fergana', '+998991234567', True);

    INSERT INTO teacher(first_name, last_name, email, phone_number, school_id) VALUES
    ('Mukhammadrizo', 'Tokhtashev', 'MT@gmail.com', '+998991425367', 1);


    INSERT INTO student(first_name, last_name, date_of_birth, gender, school_id) VALUES
    ('Safobek', 'Abdurahimov', TO_DATE('2008.22.02', 'YYYY.DD.MM'), 'Male', 1);



    INSERT INTO class(name, teacher_id, school_id) VALUES
    ('8 "A"', 1, 1);

    INSERT INTO subject(name, class_id, teacher_id) VALUES
    ('Matematics', 1, 1);

    INSERT INTO enrollment(student_id, class_id) VALUES
    (1, 1);

    INSERT INTO grade(student_id, subject_id, baho) VALUES
    (1, 1, 5);

    INSERT INTO attendance(student_id, class_id) VALUES
    (1, 1);
''')

cursor.execute('''
    SELECT
        student.first_name,
        student.last_name,
        school.name AS school_name,
        TO_CHAR(student.date_of_birth, 'dd.mm.yyyy'),
        TO_CHAR(enrollment.enrollment_date, 'dd.mm.yyyy'),
        class.name AS class_name
    FROM
        student
    JOIN school ON student.school_id = school.id
    JOIN enrollment ON student.id = enrollment.student_id
    JOIN class ON enrollment.class_id = class.id;
''')

student_info = cursor.fetchall()

for info in student_info:
    print(info)

cursor.execute('''
    ALTER TABLE school RENAME TO maktab;
    ALTER TABLE student RENAME TO talaba;
''')

cursor.execute('''SELECT * FROM maktab''')
pprint(cursor.fetchall())

cursor.execute('''SELECT * FROM talaba''')
pprint(cursor.fetchall())

cursor.execute('''
    ALTER TABLE maktab RENAME COLUMN address TO manzil;
    ALTER TABLE teacher RENAME COLUMN first_name TO ism;
    ALTER TABLE grade RENAME COLUMN grade_value TO baho;
''')

cursor.execute('''SELECT * FROM maktab''')
print(cursor.fetchall())

cursor.execute('''SELECT * FROM teacher''')
print(cursor.fetchall())

cursor.execute('''SELECT * FROM grade''')
print(cursor.fetchall())

cursor.execute('''
    ALTER TABLE talaba ADD COLUMN email VARCHAR(50) DEFAULT 'example@gmail.com';
    ALTER TABLE subject ADD COLUMN is_difficult BOOL DEFAULT True;
''')

cursor.execute('''SELECT * FROM talaba''')
print(cursor.fetchall())

cursor.execute('''SELECT * FROM subject''')
print(cursor.fetchall())

cursor.execute('''ALTER TABLE subject DROP COLUMN is_difficult''')
cursor.execute('''SELECT * FROM subject''')
print(cursor.fetchall())

cursor.execute('''
    UPDATE talaba SET first_name = 'Azizbek' WHERE id = 1;
    UPDATE talaba SET last_name = 'Ahmadjonov' WHERE id = 1;
    UPDATE maktab SET manzil = 'Ferghana' WHERE id = 1;
    UPDATE maktab SET phone_number = '+998908612907' WHERE id = 1;
''')

cursor.execute('''SELECT * FROM talaba''')
print(cursor.fetchall())

cursor.execute('''SELECT * FROM maktab''')
print(cursor.fetchall())

cursor.execute('''DELETE FROM grade WHERE id = 1''')
cursor.execute('''SELECT * FROM grade''')
print(cursor.fetchall())

cursor.execute('''DELETE FROM subject WHERE id = 1''')
cursor.execute('''SELECT * FROM subject''')
print(cursor.fetchall())

cursor.execute('''DELETE FROM student WHERE id = 1''')
cursor.execute('''SELECT * FROM student''')
print(cursor.fetchall())

cursor.execute('''DELETE FROM school WHERE id = 1''')
cursor.execute('''SELECT * FROM school''')
print(cursor.fetchall())

db.commit()
cursor.close()
db.close()
