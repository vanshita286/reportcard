from faker import Faker
import random
from .models import *

fake = Faker()

def create_subjects_marks():
    try:
        student_objs = Student.objects.all()
        subjects = Subject.objects.all()
        for student in student_objs:
            for subject in subjects:
                SubjectMarks.objects.create(
                    subject=subject,
                    student=student,
                    marks=random.randint(1, 100)
                )
    except Exception as e:
        print(e)

def seed_db(n=150) -> None:
    try:
        for _ in range(n):
            department_objs = Department.objects.all()
            random_index = random.randint(0, len(department_objs) - 1)
            department = department_objs[random_index]

            student_id = f'STU-0{random.randint(100, 999)}'
            student_name = fake.name()
            student_email = fake.email()  # Generate a fake email address
            student_age = random.randint(20, 30)
            student_address = fake.address()

            student_id_obj = StudentID.objects.create(student_id=student_id)

            student_obj = Student.objects.create(
                department=department,
                student_id=student_id_obj,
                student_name=student_name,
                student_email=student_email,
                student_age=student_age,
                student_address=student_address,
            )
    except Exception as e:
        print(e)

def generate_report_card():
    current_rank = 1
    ranks = Student.objects.annotate(marks = Sum('studentmarks__marks')).order_by('-marks','-student_age')
    i = 1
    for rank in ranks:
        ReportCard.objects.create(
            student = rank,
            student_rank=i
        )
        i=i+1