"""
Test for Models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test creating a user with an email is successfully"""

    def test_create_user_with_email(self):
        email = "test@domain.com"
        password = "testpass@123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normailized(self):
        """Test email is normalized for new user"""
        sample_emails = [
            ["test1@DOMAIN.com", "test1@domain.com"],
            ["Test2@Domain.com", "Test2@domain.com"],
            ["TEST3@DOMAIN.com", "TEST3@domain.com"],
            ["test4@domain.COM", "test4@domain.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email, password="pasowrd1234"
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a new user without an
        email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                "",
                "password",
            )

    def test_new_user_without_password_raises_error(self):
        """Test that creating user without password raises  value error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                "email@domain.COM",
                "",
            )

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            email="email@domain.com",
            password="password@123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
