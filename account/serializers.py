from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk', 'url', 'name', 'email', 'phone_number',
            'user_type', 'avatar', 'avatar_thumbnail',
        ]
        extra_kwargs = {
            'avatar': {'allow_null': True},
            'avatar_thumbnail': {'read_only': True},
            'user_type': {'read_only': True},
            'email': {'read_only': True}
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if 'avatar' in attrs:
            attrs['avatar_thumbnail'] = attrs['avatar']
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


class RegisterTeacherSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = [
            'pk', 'url', 'name', 'email', 'phone_number',
            'password', 'avatar', 'avatar_thumbnail',
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [validate_password]},
            'avatar_thumbnail': {'read_only': True},
            'name': {'required': False},
            'phone_number': {'required': False},
            'avatar': {'required': False},
        }


class MeSerializer(UserSerializer):
    pass


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
