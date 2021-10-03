import secrets

from django.contrib.auth import get_user_model

from classroom.tasks import send_temp_password_for_new_students_task

User = get_user_model()


def add_students_to_classroom(classroom, students_data):
    # Split `students_data` to groups of existing students and new students
    emails = [data['email'] for data in students_data]
    existing_students = User.students.filter(email__in=emails)
    existing_emails = [student.email for student in existing_students]

    new_students_data = list(filter(
        lambda data: data['email'] not in existing_emails,
        students_data
    ))

    # Add existing students to classroom
    classroom.students.add(*existing_students)

    # Create account for new students
    new_students = []
    temp_passwords = {}
    for data in new_students_data:
        temp_password = secrets.token_urlsafe(nbytes=8)
        temp_passwords[data['email']] = temp_password
        student = User.objects.create_student(password=temp_password, **data)
        new_students.append(student)

    classroom.students.add(*new_students)

    # Send password email to new students
    student_emails = [data['email'] for data in new_students_data]
    send_temp_password_for_new_students_task.delay(
        student_emails, temp_passwords, classroom.teacher.name
    )


def remove_students_from_classroom(classroom, student_emails):
    students_to_remove = classroom.students.filter(email__in=student_emails)
    classroom.students.remove(*students_to_remove)
