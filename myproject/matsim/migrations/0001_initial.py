# Generated by Django 4.2.10 on 2024-03-08 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chemical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mat_id', models.CharField(max_length=20)),
                ('smiles', models.CharField(max_length=100)),
                ('inchi', models.CharField(max_length=200)),
                ('formula', models.CharField(max_length=50)),
                ('charge', models.IntegerField()),
                ('num_of_heavyatom', models.IntegerField()),
                ('HOMO', models.FloatField()),
                ('LUMO', models.FloatField()),
                ('GAP', models.FloatField()),
                ('molecular_mass', models.FloatField()),
                ('multiplicity', models.IntegerField()),
                ('atoms_coord', models.JSONField()),
            ],
        ),
    ]