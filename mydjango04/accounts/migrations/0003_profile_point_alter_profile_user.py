# Generated by Django 4.2.10 on 2024-03-10 03:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_superuser_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='point',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', related_query_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
