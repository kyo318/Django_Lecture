# Generated by Django 4.2.10 on 2024-03-12 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_follower_set_user_friend_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, upload_to='profile/photo'),
        ),
    ]
