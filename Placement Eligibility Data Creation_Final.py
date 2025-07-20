# Import necessary libraries
import sqlite3
import pandas as pd
import random
from faker import Faker
import streamlit as st

fake = Faker()




# OOPs Class for generating fake data
class FakeDataGenerator:
    def __init__(self, num_students=100):
        self.num_students = num_students
        self.students = []
        self.programming = []
        self.soft_skills = []
        self.placements = []

    def generate_students(self):
        for i in range(1, self.num_students + 1):
            student_id = f"STUD{i:04d}"
            enrollment_year = random.randint(2018, 2023)
            self.students.append({
                "student_id": student_id,
                "name": fake.name(),
                "age": random.randint(18, 30),
                "gender": random.choice(['Male', 'Female']),
                "email": fake.email(),
                "phone": fake.msisdn()[:10],
                "enrollment_year": enrollment_year,
                "course_batch": random.choice(['A', 'B', 'C']),
                "city": fake.city(),
                "graduation_year": enrollment_year + 4
            })

    def generate_programming_data(self):
        counter = 1
        for student in self.students:
            PROG_ID = f'PROG{counter:03d}'
            self.programming.append({
                "programming_id": PROG_ID,
                "student_id": student["student_id"],
                "language": random.choice(["Python", "SQL", "Java"]),
                "problems_solved": random.randint(10, 200),
                "assessments_completed": random.randint(0, 10),
                "mini_projects": random.randint(0, 5),
                "certifications_earned": random.randint(0, 3),
                "latest_project_score": random.randint(50, 100)
            })
            counter += 1#To increment the counter for next programming ID
        

    def generate_soft_skills_data(self):
        counter1=1
        for student in self.students:
            SOFT_ID=f'SOFT{counter1:03d}'
            self.soft_skills.append({
                "soft_skill_id": SOFT_ID,
                "student_id": student["student_id"],
                "communication": random.randint(50, 100),
                "teamwork": random.randint(50, 100),
                "presentation": random.randint(50, 100),
                "leadership": random.randint(50, 100),
                "critical_thinking": random.randint(50, 100),
                "interpersonal_skills": random.randint(50, 100)
            })
            counter1 += 1

    def generate_placements_data(self):
        Counter2=1
        for student in self.students:
            PL_ID=f'PL{Counter2:03d}'
            status = random.choice(['Ready', 'Not Ready', 'Placed'])
            Placment_Date = fake.date_between(start_date='-10m', end_date='-1m') if status == 'Placed' else None
            self.placements.append({
                "placement_id": PL_ID,
                "student_id": student["student_id"],
                "mock_interview_score": random.randint(40, 100),
                "internships_completed": random.randint(0, 3),
                "placement_status": status,
                "company_name": fake.company() if status == "Placed" else None,
                "placement_package": random.randint(400000, 1500000) if status == "Placed" else 0,
                "interview_rounds_cleared": random.randint(0, 5),
                "placement_date": Placment_Date,
            })
            Counter2 += 1


    def generate_all(self):
        self.generate_students()
        self.generate_programming_data()
        self.generate_soft_skills_data()
        self.generate_placements_data()
        return (
            pd.DataFrame(self.students),
            pd.DataFrame(self.programming),
            pd.DataFrame(self.soft_skills),
            pd.DataFrame(self.placements)
        )



def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            student_id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender TEXT,
            email TEXT,
            phone TEXT,
            enrollment_year INTEGER,
            course_batch TEXT,
            city TEXT,
            graduation_year INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Programming (
            programming_id TEXT PRIMARY KEY,
            student_id TEXT,
            language TEXT,
            problems_solved INTEGER,
            assessments_completed INTEGER,
            mini_projects INTEGER,
            certifications_earned INTEGER,
            latest_project_score INTEGER,
            FOREIGN KEY(student_id) REFERENCES Students(student_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SoftSkills (
            soft_skill_id TEXT PRIMARY KEY,
            student_id TEXT,
            communication INTEGER,
            teamwork INTEGER,
            presentation INTEGER,
            leadership INTEGER,
            critical_thinking INTEGER,
            interpersonal_skills INTEGER,
            FOREIGN KEY(student_id) REFERENCES Students(student_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Placements (
            placement_id TEXT PRIMARY KEY,
            student_id TEXT,
            mock_interview_score INTEGER,
            internships_completed INTEGER,
            placement_status TEXT,
            company_name TEXT,
            placement_package INTEGER,
            interview_rounds_cleared INTEGER,
            placement_date TEXT,
            FOREIGN KEY(student_id) REFERENCES Students(student_id)
        )
    ''')

    conn.commit()
def insert_dataframes_to_sqlite(conn, df_students, df_programming, df_soft_skills, df_placements):
	df_students.to_sql('Students', conn, if_exists='replace', index=False)
	df_programming.to_sql('Programming', conn, if_exists='replace', index=False)
	df_soft_skills.to_sql('SoftSkills', conn, if_exists='replace', index=False)
	df_placements.to_sql('Placements', conn, if_exists='replace', index=False)


# SQLite Connection
conn = sqlite3.connect("placement_eligibility.db")

create_tables(conn)

generator = FakeDataGenerator(num_students=500)
df_students, df_programming, df_soft_skills, df_placements = generator.generate_all()

insert_dataframes_to_sqlite(conn, df_students, df_programming, df_soft_skills, df_placements)

# Close connection
conn.close()

print("Data inserted successfully into SQLite.")

