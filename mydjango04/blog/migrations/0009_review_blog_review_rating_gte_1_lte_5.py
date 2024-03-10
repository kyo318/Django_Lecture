# Generated by Django 4.2.10 on 2024-03-08 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_review_alter_post_options'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='review',
            constraint=models.CheckConstraint(check=models.Q(('rating__gte', 1), ('rating__lte', 5)), name='blog_review_rating_gte_1_lte_5'),
        ),
    ]