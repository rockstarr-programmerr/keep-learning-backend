import secrets

from django.contrib.auth import get_user_model

User = get_user_model()


def add_students_to_classroom(classroom, students_data):
    # Split `students_data` to groups of existing students and new students
    emails = [data['email'] for data in students_data]
    existing_students = User.students.filter(email__in=emails)
    existing_emails = [student.email for student in existing_students]

    new_students_data = filter(
        lambda data: data['email'] not in existing_emails,
        students_data
    )

    # Add existing students to classroom
    classroom.students.add(*existing_students)

    # Create account for new students
    new_students = []
    for data in new_students_data:
        temp_password = secrets.token_urlsafe(nbytes=8)
        student = User.objects.create_student(password=temp_password, **data)
        new_students.append(student)

    classroom.students.add(*new_students)

    # Send password email to new students
    # TODO
