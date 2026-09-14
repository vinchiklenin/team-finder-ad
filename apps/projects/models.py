from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", _("Открыт")
        CLOSED = "closed", _("Закрыт")

    name = models.CharField(max_length=200, verbose_name=_("Название проекта"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name=_("Автор"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    github_url = models.URLField(blank=True, verbose_name=_("Ссылка на GitHub"))
    status = models.CharField(
        max_length=6,
        choices=Status.choices,
        default=Status.OPEN,
        verbose_name=_("Статус"),
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_projects",
        blank=True,
        verbose_name=_("Участники"),
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name
