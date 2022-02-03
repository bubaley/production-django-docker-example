from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core import exceptions


def validate_user_password(password):
    try:
        validate_password(password)
    except exceptions.ValidationError as e:
        serializer_error = serializers.as_serializer_error(e)
        raise serializers.ValidationError(serializer_error["non_field_errors"])
    return password
