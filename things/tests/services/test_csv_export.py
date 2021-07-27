import pytest
from things.services import csv_export
from unittest.mock import patch
from things.tests.factories import ThingFactory

pytestmark = pytest.mark.django_db

@patch("things.services.CSV_FOLDER", "media/tests/csv_export/")
def test_export__success():
    ThingFactory.create_batch(10)
    filename = "aaa.csv"
    csv_export(filename)
    # with open
    # DictReader
    # keys = thing_fields
    # len(keys) = len(thing_fields)

