from things.models import Thing
import pytest
from things.services import csv_import
from unittest.mock import patch
import csv
from things.tests.factories import ThingFactory, UserFactory, SectionFactory
from tags.tests.factories import TagFactory

pytestmark = pytest.mark.django_db

@patch("things.services.CSV_FOLDER", "media/tests/csv_import/")
def test_import_fields_without_m2m__success():
    UserFactory(username = "admin")
    SectionFactory(title="Монетки")
    TagFactory(title="Фантики")
    TagFactory(title="Вещи")
    filename = "test_import.csv"
    csv_import(filename)
    with open(f"media/tests/csv_import/{filename}", "r", encoding="utf-8") as f:
        fieldnames = ["title", "content", "state", "owner__username", "section__title", "tags", "comments"]
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=";")
        things_from_db = list(Thing.objects.values("title", "content", "state", "owner__username", "section__title", "comments"))[::-1]
        for i, row in enumerate(reader):
            row.pop("tags")
            assert row == things_from_db[i]


@patch("things.services.CSV_FOLDER", "media/tests/csv_import/")
def test_import_fields_tags__success():
    UserFactory(username = "admin")
    SectionFactory(title="Монетки")
    TagFactory(title="Фантики")
    TagFactory(title="Вещи")
    filename = "test_import.csv"
    csv_import(filename)
    with open(f"media/tests/csv_import/{filename}", "r", encoding="utf-8") as f:
        fieldnames = ["title", "content", "state", "owner__username", "section__title", "tags", "comments"]
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=";")
        things_from_db = list(Thing.objects.all())[::-1]
        for i, row in enumerate(reader):
            row_tags = row.pop("tags").split(",")
            assert list(things_from_db[i].tags.values_list("title", flat=True)) == row_tags