import pytest
from things.services import csv_export
from unittest.mock import patch
import csv
from things.tests.factories import ThingFactory

pytestmark = pytest.mark.django_db

@patch("things.services.CSV_FOLDER", "media/tests/csv_export/")
def test_export_len_keys__success():
    ThingFactory.create_batch(5)
    filename = "test_export.csv"
    csv_export(filename)
    with open(f"media/tests/csv_export/{filename}", "r", encoding="utf-8") as f:
        fieldnames = ['#', 'title', 'content', 'state', 'section', 'date_published', 'image', 'is_sold', 'owner', 'tags', 'comments']
        reader = csv.DictReader(f, fieldnames=None, delimiter=";")
        assert len(next(reader).keys()) == len(fieldnames)


@patch("things.services.CSV_FOLDER", "media/tests/csv_export/")
def test_export_check_row_number__success():
    ThingFactory.create_batch(5)
    filename = "test_export.csv"
    csv_export(filename)
    with open(f"media/tests/csv_export/{filename}", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, fieldnames=None, delimiter=";")
        row_numbers = list(range(0, 5))
        expected_row_numbers = [int(row["#"]) for row in reader]
        assert row_numbers == expected_row_numbers
        assert len(row_numbers) == len(expected_row_numbers)


@patch("things.services.CSV_FOLDER", "media/tests/csv_export/")
def test_export_check_field_thing_values__success():
    things = ThingFactory.create_batch(5)
    filename = "test_export.csv"
    csv_export(filename)
    with open(f"media/tests/csv_export/{filename}", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, fieldnames=None, delimiter=";")
        for i, row in enumerate(reader):
            print(row)
            print(things[i].__dict__)
            print("*"*7)