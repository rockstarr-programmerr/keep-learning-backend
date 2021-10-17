import secrets

from django.conf import settings
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


def add_reading_exercises_to_classroom(classroom, exercise_pks, user):
    exercises = user.reading_exercises_created.filter(pk__in=exercise_pks)
    classroom.reading_exercises.add(*exercises)


def remove_reading_exercises_to_classroom(classroom, exercise_pks):
    classroom.reading_exercises.remove(*exercise_pks)


def resend_password_emails(classroom, email):
    student = User.students.filter(email=email).first()

    # If `last_login` is not None, meaning student already logged in successfully
    # so don't touch their password
    if not student or student.last_login:
        return

    temp_password = secrets.token_urlsafe(nbytes=8)
    student.set_password(temp_password)
    student.save()

    temp_passwords = {email: temp_password}

    send_temp_password_for_new_students_task.delay(
        [email], temp_passwords, classroom.teacher.name
    )


def upload_reading_exercise_image(image, request=None):
    path = settings.MEDIA_ROOT / 'classroom' / 'reading_exercises' / 'uploaded_images' / image.name
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        unique_name = path.stem + secrets.token_urlsafe(nbytes=8)
        path = path.parent / f'{unique_name}{path.suffix}'

    with open(path, 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    rpath = path.relative_to(settings.BASE_DIR)
    url = '/' + str(rpath).replace('\\', '/')
    if request:
        url = request.build_absolute_uri(url)
    return url
