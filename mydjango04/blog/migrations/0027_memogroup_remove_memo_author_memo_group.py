# Generated by Django 4.2.11 on 2024-03-17 07:57

from django.db import migrations, models
import django.db.models.deletion


def delete_memos(apps, schema_editor):
    Memo = apps.get_model("blog", "Memo")
    Memo.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0026_memo_author"),
    ]

    operations = [
        migrations.RunPython(delete_memos, migrations.RunPython.noop),
        migrations.CreateModel(
            name="MemoGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name="memo",
            name="author",
        ),
        migrations.AddField(
            model_name="memo",
            name="group",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="blog.memogroup",
            ),
            preserve_default=False,
        ),
    ]
