import io

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.files.images import ImageFile
from django.utils.translation import gettext as _
from PIL import Image
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk', 'url', 'name', 'email', 'phone_number',
            'user_type', 'avatar', 'avatar_thumbnail',
            'last_login',
        ]
        extra_kwargs = {
            'avatar': {'allow_null': True},
            'avatar_thumbnail': {'read_only': True},
            'user_type': {'read_only': True},
            'email': {'read_only': True},
            'last_login': {'read_only': True},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if 'avatar' in attrs:
            avatar = attrs['avatar']
            if avatar:
                attrs['avatar'] = self._make_thumbnail(avatar, 256, 256)
                attrs['avatar_thumbnail'] = self._make_thumbnail(avatar, 64, 64)
            else:
                attrs['avatar_thumbnail'] = avatar  # When remove avatar, also remove avatar_thumbnail
        return attrs

    def validate_avatar(self, img):
        if not img:
            return img

        size = img.size / 1e6  # bytes to megabytes
        if size > settings.MAX_UPLOAD_SIZE_MEGABYTES:
            raise serializers.ValidationError(
                _('File size must not exceed %dMB.') % settings.MAX_UPLOAD_SIZE_MEGABYTES,
                code='exceed_max_upload_size'
            )

        return img

    @staticmethod
    def _make_thumbnail(image, width, height):
        thumb = Image.open(image)
        thumb.thumbnail((width, height))

        buffer = io.BytesIO()
        thumb.save(buffer, format=thumb.format)

        data = ImageFile(buffer, name=image.name)
        return data


class RegisterTeacherSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = [
            'pk', 'url', 'name', 'email', 'phone_number',
            'user_type', 'avatar', 'avatar_thumbnail',
            'last_login', 'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [validate_password]},
            'avatar_thumbnail': {'read_only': True},
            'name': {'required': False},
            'phone_number': {'required': False},
            'avatar': {'required': False},
        }
        read_only_fields = [
            'avatar_thumbnail', 'user_type', 'last_login'
        ]


class MeSerializer(UserSerializer):
    pass


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)


class EmailResetPasswordLinkSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, validators=[validate_password])


class EmailResetPasswordLinkTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'date_joined']
