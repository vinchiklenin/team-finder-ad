from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Project(models.Model):
    name = models.CharField(max_length=30, verbose_name=_('Имя проекта'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Описание'))
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name=_('Автор')
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    url = models.URLField(blank=True, null=True, verbose_name=_('Ссылка на GitHub'))
    status = models.CharField(max_length=max(len(status[0]) for status in PROJECT_STATUS_CHOICES), choices=PROJECT_STATUS_CHOICES, default=PROJECT_STATUS_OPEN, verbose_name=_('Статус'))
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participating_projects', blank=True, verbose_name=_('Участники'))
                                   
    