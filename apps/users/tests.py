from django.contrib.auth.hashers import make_password
from django.test import TestCase

from .forms import ProfileForm, RegistrationForm
from .models import User


class UserFormTests(TestCase):
    def test_registration_creates_user_with_hashed_password(self):
        form = RegistrationForm(
            data={
                "name": "Иван",
                "surname": "Иванов",
                "email": "IVAN@EXAMPLE.COM",
                "password": "safe-password-123",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        user = form.save(commit=False)

        self.assertEqual(user.email, "ivan@example.com")
        self.assertTrue(user.check_password("safe-password-123"))
        self.assertFalse(user.avatar.name)

    def test_profile_rejects_invalid_github_url(self):
        user = User.objects.create(
            email="person@example.com",
            password=make_password("safe-password-123"),
            name="Тест",
            surname="Тестов",
            avatar="avatars/test.png",
        )
        form = ProfileForm(
            data={
                "name": user.name,
                "surname": user.surname,
                "about": "",
                "github_url": "https://github.com.example.org/openai",
            },
            user=user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("github_url", form.errors)
