from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="username",
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True, verbose_name="Почта"),
        ),
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(max_length=124, verbose_name="Имя"),
        ),
        migrations.AlterField(
            model_name="user",
            name="surname",
            field=models.CharField(max_length=124, verbose_name="Фамилия"),
        ),
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.ImageField(upload_to="avatars/", verbose_name="Аватар"),
        ),
        migrations.AddField(
            model_name="user",
            name="phone",
            field=models.CharField(max_length=12, unique=True, verbose_name="Телефон"),
        ),
        migrations.AddField(
            model_name="user",
            name="github_url",
            field=models.URLField(blank=True, verbose_name="Ссылка на GitHub"),
        ),
        migrations.AddField(
            model_name="user",
            name="about",
            field=models.CharField(blank=True, max_length=256, verbose_name="О себе"),
        ),
        migrations.AddField(
            model_name="user",
            name="favorites",
            field=models.ManyToManyField(blank=True, related_name="interested_users", to="projects.project", verbose_name="Избранные проекты"),
        ),
    ]
