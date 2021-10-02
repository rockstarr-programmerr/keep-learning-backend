from django.contrib.auth.models import UserManager


def get_first_part_of_email(email):
    return email.split('@')[0]


class CustomUserManager(UserManager):
    """
    Customize to allow creating user with just email, no need username
    """
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        assert bool(email), 'Email is required for creating user.'
        username = get_first_part_of_email(email)
        return super().create_user(username, email=email, password=password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        assert bool(email), 'Email is required for creating user.'
        username = get_first_part_of_email(email)
        if not 'user_type' in extra_fields:
            user_type = 'admin'  # TODO: how to be dynamic?
            extra_fields['user_type'] = user_type
        return super().create_superuser(username, email=email, password=password, **extra_fields)
