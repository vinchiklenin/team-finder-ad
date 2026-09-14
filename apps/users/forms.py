from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from team_finder.validators import validate_github_url

from .models import User


class RegistrationForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=124)
    surname = forms.CharField(label="Фамилия", max_length=124)
    email = forms.EmailField(label="Почта")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean_email(self) -> str:
        email = User.objects.normalize_email(self.cleaned_data["email"]).lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Пользователь с такой почтой уже существует.")
        return email

    def clean_password(self) -> str:
        password = self.cleaned_data["password"]
        password_validation.validate_password(password)
        return password

    def save(self, commit: bool = True) -> User:
        user = User(
            name=self.cleaned_data["name"],
            surname=self.cleaned_data["surname"],
            email=self.cleaned_data["email"],
        )
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean_email(self) -> str:
        return User.objects.normalize_email(self.cleaned_data["email"]).lower()


class ProfileForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=124)
    surname = forms.CharField(label="Фамилия", max_length=124)
    avatar = forms.ImageField(label="Аватар", required=False)
    about = forms.CharField(label="О себе", max_length=256, required=False, widget=forms.Textarea)
    github_url = forms.URLField(label="Ссылка на GitHub", required=False)

    def __init__(self, *args, user: User, **kwargs):
        self.user = user
        if "initial" not in kwargs:
            kwargs["initial"] = {
                "name": user.name,
                "surname": user.surname,
                "avatar": user.avatar,
                "about": user.about,
                "github_url": user.github_url,
            }
        super().__init__(*args, **kwargs)

    def clean_github_url(self) -> str:
        return validate_github_url(self.cleaned_data["github_url"])

    def save(self) -> User:
        self.user.name = self.cleaned_data["name"]
        self.user.surname = self.cleaned_data["surname"]
        self.user.about = self.cleaned_data["about"]
        self.user.github_url = self.cleaned_data["github_url"]
        if self.cleaned_data["avatar"]:
            self.user.avatar = self.cleaned_data["avatar"]
        self.user.save()
        return self.user


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="Текущий пароль", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Подтвердите новый пароль", widget=forms.PasswordInput)

    def __init__(self, *args, user: User, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self) -> str:
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError("Текущий пароль указан неверно.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error("new_password2", "Пароли не совпадают.")
        if new_password1:
            password_validation.validate_password(new_password1, self.user)
        return cleaned_data

    def save(self) -> User:
        self.user.set_password(self.cleaned_data["new_password1"])
        self.user.save()
        return self.user
