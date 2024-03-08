# Generated by Django 4.2.10 on 2024-03-07 13:56

from django.db import migrations
import csv
from typing import Dict, Iterator, Tuple

from django.db import migrations
import itertools

CSV_PATH = "shop/assets/zipcode_db/20231205/서울특별시.txt"


def get_code_and_name_from_csv(zipcode_csv_path: str) -> Iterator[Tuple[str, str]]:
    with open(zipcode_csv_path, "rt", encoding="utf-8-sig") as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter="|")
        row: Dict
        for row in csv_reader:
            code = row["우편번호"]
            name = "{시도} {시군구} {도로명}".format(**row)
            yield code, name


def get_chunks(iterable: Iterator, chunk_size: int = 100) -> Iterator:
    iterator = iterable if hasattr(iterable, "__next__") else iter(iterable)

    for first in iterator:
        yield itertools.chain([first], itertools.islice(iterator, chunk_size - 1))


def add_zipcode_data(apps, schema_editor):
    ZipCode = apps.get_model("shop", "ZipCode")
    zipcode_list = (
        ZipCode(code=code, name=name)
        for code, name in get_code_and_name_from_csv(CSV_PATH)
    )
    for chunks in get_chunks(zipcode_list, chunk_size=1000):
        print("chunk size:", len(list(chunks)))
        ZipCode.objects.bulk_create(chunks)


def remove_zipcode_data(apps, schema_editor):
    ZipCode = apps.get_model("shop", "ZipCode")
    ZipCode.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_zipcode_data, remove_zipcode_data),
    ]
