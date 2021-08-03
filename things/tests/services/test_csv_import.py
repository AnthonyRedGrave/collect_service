from things.models import Thing
import pytest
from things.services import csv_import
from unittest.mock import patch
import csv
from django.contrib.auth.models import User
from things.tests.factories import UserFactory, SectionFactory
from tags.tests.factories import TagFactory
from tags.models import Tag
from rest_framework.validators import ValidationError

pytestmark = pytest.mark.django_db


@patch("things.services.CSV_FOLDER", "media/tests/csv_import/")
def test_import_fields_without_m2m__success():
    count_before = Thing.objects.count()
    UserFactory(username="admin")
    SectionFactory(title="Монетки")
    TagFactory(title="Фантики")
    TagFactory(title="Вещи")
    filename = "test_import.csv"
    csv_import(filename)
    count_after = Thing.objects.count()
    with open(f"media/tests/csv_import/{filename}", "r", encoding="utf-8") as f:
        fieldnames = [
            "title",
            "content",
            "state",
            "owner__username",
            "section__title",
            "tags",
            "comments",
        ]
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=";")
        things_from_db = list(
            Thing.objects.values(
                "title",
                "content",
                "state",
                "owner__username",
                "section__title",
                "comments",
            )
        )[::-1]
        for i, row in enumerate(reader):
            row.pop("tags")
            assert row == things_from_db[i]
        assert count_before + 3 == count_after


@patch("things.services.CSV_FOLDER", "media/tests/csv_import/")
def test_import_fields_tags__success():
    UserFactory(username="admin")
    SectionFactory(title="Монетки")
    TagFactory(title="Вещи")
    TagFactory(title="Фантики")
    filename = "test_import.csv"
    csv_import(filename)
    with open(f"media/tests/csv_import/{filename}", "r", encoding="utf-8") as f:
        fieldnames = [
            "title",
            "content",
            "state",
            "owner__username",
            "section__title",
            "tags",
            "comments",
        ]
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=";")
        things_from_db = list(Thing.objects.all())[::-1]
        for i, row in enumerate(reader):
            row_tags = sorted(row.pop("tags").split(","))
            assert list(things_from_db[i].tags.values_list("title", flat=True)) == row_tags


@patch("things.services.CSV_FOLDER", "media/tests/csv_import/")
def test_import_fields_tags__error():
    UserFactory(username="admin")
    SectionFactory(title="Монетки")
    TagFactory(title="Вещи")
    TagFactory(title="Фантики")
    filename = "test_import_wrong_tags.csv"

    tags = list(Tag.objects.values_list("title", flat=True))
    with pytest.raises(ValidationError):
        csv_import(filename)
    with open(f"media/tests/csv_import/{filename}", "r", encoding="utf-8") as f:
        fieldnames = [
            "title",
            "content",
            "state",
            "owner__username",
            "section__title",
            "tags",
            "comments",
        ]
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=";")
        row_tags = next(reader)["tags"].split(",")
        assert row_tags not in tags


@patch("things.services.CSV_FOLDER", "media/tests/csv_import/")
def test_import_fields_user__error():
    UserFactory(username="admin")
    SectionFactory(title="Монетки")
    TagFactory(title="Вещи")
    TagFactory(title="Фантики")
    filename = "test_import_wrong_owner.csv"

    users = list(User.objects.values_list("username", flat=True))
    with pytest.raises(ValidationError):
        csv_import(filename)
    with open(f"media/tests/csv_import/{filename}", "r", encoding="utf-8") as f:
        fieldnames = [
            "title",
            "content",
            "state",
            "owner",
            "section__title",
            "tags",
            "comments",
        ]
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=";")
        row_owner = next(reader)["owner"]
        assert row_owner not in users
