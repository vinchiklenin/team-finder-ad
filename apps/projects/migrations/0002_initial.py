import django.db.models.deletion

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='create_time',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='url',
            new_name='github_url',
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_projects', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='project',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participated_projects', to=settings.AUTH_USER_MODEL, verbose_name='Участники'),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('open', 'Открыт'), ('closed', 'Закрыт')], default='open', max_length=6, verbose_name='Статус'),
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ('-created_at',)},
        ),
    ]
