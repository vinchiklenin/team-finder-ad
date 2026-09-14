from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_user_profile_and_favorites"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[],
        ),
    ]
