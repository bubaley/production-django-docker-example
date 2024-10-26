from air_drf_relation.serializers import AirModelSerializer
from django.db import transaction
from rest_framework import serializers

from user.functions.validate_user_password import validate_user_password
from user.models import User


class UserSerializer(AirModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'is_staff',
            'last_name',
            'phone',
            'password',
        )
        read_only_fields = ('is_superuser', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        updating = True if getattr(self, 'instance') else False
        if updating:
            self.fields.pop('password')

    @staticmethod
    def validate_password(value):
        validate_user_password(password=value)
        return value

    def create(self, validated_data):
        with transaction.atomic():
            password = validated_data.pop('password')
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
        return user
