from django.contrib.auth import get_user_model

User = get_user_model()


def register_teacher(data):
    email = data.pop('email')
    password = data.pop('password')
    teacher = User.objects.create_teacher(email=email, password=password, **data)
    return teacher
