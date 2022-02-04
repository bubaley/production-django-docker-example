from django.db import transaction
from rest_framework import serializers
from user.models import User
from user.services import validate_user_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'is_superuser', 'last_name', 'phone', 'password')
        read_only_fields = ('is_superuser',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        updating = True if getattr(self, 'instance') else False
        if updating:
            self.fields.pop('password')

    def validate_password(self, value):
        validate_user_password(password=value)
        return value

    def create(self, validated_data):
        with transaction.atomic():
            password = validated_data.pop('password')
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
        return user
