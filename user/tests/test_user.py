# Create your tests here.

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import serializers

from user.functions.validate_user_password import validate_user_password
from user.orm.get_users import get_active_users

User = get_user_model()


class UserPasswordValidationTests(TestCase):
    """Tests for password validation function."""

    def test_validate_strong_password_success(self):
        """Test that a strong password passes validation."""
        strong_password = 'SecurePassword123!'
        # Should not raise any exception
        result = validate_user_password(strong_password)
        self.assertEqual(result, strong_password)

    def test_validate_weak_password_raises_error(self):
        """Test that a weak password raises ValidationError."""
        weak_password = '123'
        with self.assertRaises(serializers.ValidationError):
            validate_user_password(weak_password)

    def test_validate_common_password_raises_error(self):
        """Test that a common password raises ValidationError."""
        common_password = 'password'
        with self.assertRaises(serializers.ValidationError):
            validate_user_password(common_password)


class GetActiveUsersTests(TestCase):
    """Tests for getting active users function."""

    def setUp(self):
        """Set up test data."""
        # Create active users
        User.objects.create(
            email='active1@example.com',
            first_name='Active',
            last_name='User1',
            phone='+1234567890',
            password='TestPassword123!',
            is_active=True,
        )
        User.objects.create(
            email='active2@example.com',
            first_name='Active',
            last_name='User2',
            phone='+1234567891',
            password='TestPassword123!',
            is_active=True,
        )
        # Create inactive user
        User.objects.create(
            email='inactive@example.com',
            first_name='Inactive',
            last_name='User',
            phone='+1234567892',
            password='TestPassword123!',
            is_active=False,
        )

    def test_get_active_users_returns_only_active(self):
        """Test that get_active_users returns only active users."""
        active_users = get_active_users()
        self.assertEqual(active_users.count(), 2)
        for user in active_users:
            self.assertTrue(user.is_active)

    def test_get_active_users_excludes_inactive(self):
        """Test that get_active_users excludes inactive users."""
        active_users = get_active_users()
        inactive_emails = [user.email for user in active_users if not user.is_active]
        self.assertEqual(len(inactive_emails), 0)
