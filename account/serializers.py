from django.contrib.auth import get_user_model
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
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if 'avatar' in attrs:
            attrs['avatar_thumbnail'] = attrs['avatar']
        return attrs

    def validate_avatar(self, img):
        return img  # TODO


class RegisterTeacherSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = [
            'pk', 'url', 'name', 'email', 'phone_number',
            'password', 'avatar', 'avatar_thumbnail',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'avatar_thumbnail': {'read_only': True},
            'name': {'required': False},
            'phone_number': {'required': False},
            'avatar': {'required': False},
        }


class MeSerializer(UserSerializer):
    pass
