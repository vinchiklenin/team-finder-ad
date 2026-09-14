from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="github_url",
            field=models.URLField(blank=True, default="", verbose_name="Ссылка на GitHub"),
            preserve_default=False,
        ),
    ]
