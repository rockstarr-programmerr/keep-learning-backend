from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template import loader


@shared_task
def send_temp_password_for_new_students_task(student_emails, temp_passwords, teacher_name):
    return send_temp_password_for_new_students(student_emails, temp_passwords, teacher_name)

def send_temp_password_for_new_students(student_emails, temp_passwords, teacher_name):
    if not student_emails:
        return 0

    messages = []
    for student_email in student_emails:
        temp_password = temp_passwords[student_email]

        context = {
            'url': settings.WEB_LOGIN_URL,
            'student_email': student_email,
            'teacher_name': teacher_name,
            'temp_password': temp_password,
            'site_name': 'Tango',
        }

        title = loader.render_to_string('classroom/temp_passwords/email_title.txt', context)
        title = title.replace('\n', '')  # Title cannot have newline
        message = loader.render_to_string('classroom/temp_passwords/email_body.txt', context)
        html_message = loader.render_to_string('classroom/temp_passwords/email_body.html', context)

        message = EmailMultiAlternatives(
            title,
            message,
            alternatives=[
                (html_message, 'text/html')
            ],
            to=[student_email],
        )
        messages.append(message)

    connection = get_connection()
    return connection.send_messages(messages)
