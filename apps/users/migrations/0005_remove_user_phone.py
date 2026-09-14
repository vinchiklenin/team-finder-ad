from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
    ]
