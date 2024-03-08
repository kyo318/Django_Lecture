import string
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.crypto import get_random_string


def create_user_if_empty(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    is_existed = User.objects.filter(pk=1).exists()
    if is_existed is False:
        random_username = "auto-" + get_random_string(
            length=10, allowed_chars=string.ascii_letters
        )
        user = User.objects.create_user(
            username=random_username, password=None, is_active=False, pk=1
        )
        print("auto_generated_user created (pk=1):", user)


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_user_if_empty,  # 정방향
            migrations.RunPython.noop,  # 역방향
        ),
        migrations.AddField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
