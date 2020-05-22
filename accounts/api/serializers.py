from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    email2 = serializers.EmailField(label='Confirm email')

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'email2'
        ]
        extra_kwargs = {'password':
                            {'write_only': True}
                        }

    def validate_email2(self, value):
        data = self.get_initial()
        email = data.get('email')
        email2 = value
        if email != email2:
            raise ValidationError('Emails do not match.')
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError('User already registered.')
        return value

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        user_obj = User(username=username)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    email = serializers.EmailField(label='Email address', allow_blank=True, required=False)
    username = serializers.CharField(allow_blank=True, required=False)
    token = serializers.CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'token'
        ]
        extra_kwargs = {'password':
                            {'write_only': True}
                        }

    def validate(self, data):
        user_obj = None
        email = data.get('email', None)
        username = data.get('username', None)
        password = data['password']
        if not email and not username:
            raise ValidationError('A username or email is required')
        user = User.objects.filter(
            Q(email=email) |
            Q(username=username),
            ~Q(email__iexact='')
        ).distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError('this username/email is not valid')
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError('Incorrect credentials please try again.')
            data['token'] = 'SOME RANDOM TOKEN'
            return data


class UserRetrieveSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
        ]
