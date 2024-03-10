# Generated by Django 4.2.10 on 2024-03-10 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_remove_post_tag_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tag_set',
            field=models.ManyToManyField(blank=True, related_name='blog_post_set', related_query_name='blog_post', through='blog.PostTagRelation', to='blog.tag'),
        ),
    ]
