from __future__ import annotations

from io import BytesIO
from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str | None = None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField("Почта", unique=True)
    name = models.CharField("Имя", max_length=124)
    surname = models.CharField("Фамилия", max_length=124)
    avatar = models.ImageField("Аватар", upload_to="avatars/")
    github_url = models.URLField("Ссылка на GitHub", blank=True)
    about = models.CharField("О себе", max_length=256, blank=True)
    favorites = models.ManyToManyField(
        "projects.Project",
        related_name="interested_users",
        blank=True,
        verbose_name="Избранные проекты",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.name} {self.surname} <{self.email}>"

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar.save(
                f"avatar_{uuid4().hex}.png",
                ContentFile(self._build_initial_avatar()),
                save=False,
            )
        super().save(*args, **kwargs)

    def _build_initial_avatar(self) -> bytes:
        from PIL import Image, ImageDraw, ImageFont

        palette = ("#6B7280", "#64748B", "#78716C", "#4B5563", "#475569")
        color = palette[sum(map(ord, self.email or self.name or "?")) % len(palette)]
        image = Image.new("RGB", (256, 256), color)
        draw = ImageDraw.Draw(image)
        font_path = Path(settings.BASE_DIR) / "static" / "fonts" / "Neue_Haas_Grotesk_Display_Pro_75_Bold.otf"
        try:
            font = ImageFont.truetype(font_path, 128)
        except OSError:
            font = ImageFont.load_default()

        initial = (self.name or "?").strip()[:1].upper() or "?"
        draw.text((128, 128), initial, font=font, fill="white", anchor="mm")

        output = BytesIO()
        image.save(output, format="PNG")
        return output.getvalue()
