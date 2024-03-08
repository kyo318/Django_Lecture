import os
import csv
from typing import Dict, Iterator, Tuple
from urllib.request import urlretrieve
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


def get_code_and_name_from_csv(zipcode_csv_path: str) -> Iterator[Tuple[str, str]]:
    with open(zipcode_csv_path, "rt", encoding="utf-8-sig") as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter="|")
        row: Dict
        for row in csv_reader:
            code = row["우편번호"]
            name = "{시도} {시군구} {도로명}".format(**row)
            yield code, name


def main():
    sample_csv_url = "https://raw.githubusercontent.com/pyhub-kr/dump-data/main/zipcode_db/20231205/%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C-5000%ED%96%89.txt"
    csv_path = "shop/assets/zipcode_db/20231205/서울특별시.txt"

    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    # 파일을 저장할 폴더를 생성해줍니다.
    urlretrieve(sample_csv_url, csv_path)
    generator = get_code_and_name_from_csv(csv_path)

    print(next(generator))
    print(next(generator))
    print(next(generator))


if __name__ == "__main__":
    main()
