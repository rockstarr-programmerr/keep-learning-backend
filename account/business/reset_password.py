from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from account.serializers import EmailResetPasswordLinkTaskSerializer
from account.tasks import send_email_reset_password_link_task
from keep_learning.utils.url import update_url_params

User = get_user_model()


class ResetPasswordTokenInvalid(Exception):
    pass


class ResetPasswordBusiness:
    token_generator = PasswordResetTokenGenerator()

    def __init__(self, user):
        self.user = user

    def send_email(self):
        url = self.get_link()
        serializer = EmailResetPasswordLinkTaskSerializer(instance=self.user)
        send_email_reset_password_link_task.delay(serializer.data, url)

    def reset_password(self, password, token):
        self.check_token(token)
        self.user.set_password(password)
        self.user.save()

    def get_link(self):
        token = self.token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        url = update_url_params(settings.WEB_RESET_PASSWORD_URL, {'token': token, 'uid': uid})
        return url

    def check_token(self, token):
        is_valid = self.token_generator.check_token(self.user, token)
        if not is_valid:
            raise ResetPasswordTokenInvalid

    @staticmethod
    def get_user_by_email(email):
        return User.objects.filter(email=email).first()

    @staticmethod
    def get_user_by_uid(uid):
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user
