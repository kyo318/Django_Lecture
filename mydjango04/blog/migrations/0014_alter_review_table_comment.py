# Generated by Django 4.2.10 on 2024-03-08 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_post_options'),
    ]

    operations = [
        migrations.AlterModelTableComment(
            name='review',
            table_comment='사용자 리뷰와 평점을 저장하는 테이블',
        ),
    ]