# Generated by Django 4.2.10 on 2024-03-14 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weblog', '0003_post_content_post_created_date_post_photo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='ip',
            field=models.GenericIPAddressField(default='127.0.0.1'),
            preserve_default=False,
        ),
    ]