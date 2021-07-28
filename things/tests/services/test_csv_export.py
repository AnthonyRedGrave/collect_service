import pytest
from things.services import csv_export
from unittest.mock import patch
import csv
from things.tests.factories import ThingFactory
import datetime

pytestmark = pytest.mark.django_db

@patch("things.services.CSV_FOLDER", "media/tests/csv_export/")
def test_export_len_keys__success():
    ThingFactory.create_batch(5)
    filename = "test_export_len_keys.csv"
    csv_export(filename)
    with open(f"media/tests/csv_export/{filename}", "r", encoding="utf-8") as f:
        fieldnames = ['#', 'title', 'content', 'state', 'section', 'date_published', 'image', 'is_sold', 'owner', 'tags', 'comments']
        reader = csv.DictReader(f, fieldnames=None, delimiter=";")
        assert len(next(reader).keys()) == len(fieldnames)


@patch("things.services.CSV_FOLDER", "media/tests/csv_export/")
def test_export_check_row_number__success():
    ThingFactory.create_batch(5)
    filename = "test_export_row_number.csv"
    csv_export(filename)
    with open(f"media/tests/csv_export/{filename}", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, fieldnames=None, delimiter=";")
        row_numbers = list(range(0, 5))
        expected_row_numbers = [int(row["#"]) for row in reader]
        assert row_numbers == expected_row_numbers
        assert len(row_numbers) == len(expected_row_numbers)


@patch("things.services.CSV_FOLDER", "media/tests/csv_export/")
def test_export_check_fields_title_content_state_section_thing_values__success():
    things = ThingFactory.create_batch(5)
    filename = "test_export_some_fields.csv"
    csv_export(filename)
    with open(f"media/tests/csv_export/{filename}", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, fieldnames=None, delimiter=";")
        for i, row in enumerate(reader):
            int_list_date = [int(el) for el in row['date_published'].split('-')]
            
            assert things[i].title == row['title']
            assert things[i].content == row['content']
            assert things[i].state == row['state']
            assert things[i].section.__str__() == row['section']
            assert things[i].date_published == datetime.date(*int_list_date)
            assert things[i].owner.username == row['owner']


@patch("things.services.CSV_FOLDER", "media/tests/csv_export/")
def test_export_check_fields_comments__success():
    things = ThingFactory.create_batch(5, tags=5, comments=3)
    filename = "test_export_comments.csv"
    csv_export(filename)
    with open(f"media/tests/csv_export/{filename}", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, fieldnames=None, delimiter=";")
        for i, row in enumerate(reader):
            row_comments = row['comments'].split(';')
            thing_comments = list(things[i].comments.values_list("content", flat=True))
            assert len(row_comments) == len(thing_comments)
            assert row_comments == thing_comments


@patch("things.services.CSV_FOLDER", "media/tests/csv_export/")
def test_export_check_fields_tags__success():
    things = ThingFactory.create_batch(5, tags=5, comments=3)
    filename = "test_export_tags.csv"
    csv_export(filename)
    with open(f"media/tests/csv_export/{filename}", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, fieldnames=None, delimiter=";")
        for i, row in enumerate(reader):
            row_tags = row['tags'].split(';')
            thing_tags = list(things[i].tags.values_list("title", flat=True))
            assert len(row_tags) == len(thing_tags)
            assert row_tags == thing_tags