import pytest
from rest_framework import serializers
from collect_api.tests.factories import SectionFactory
from pytest_factoryboy import register
from collect_api.serializers import SectionSerializer

register(SectionFactory)

@pytest.mark.parametrize("title", [("Монетки"), ("Фантики")])
def test_section_serializer(title):
    data = {
        'title': title
    }
    serializer = SectionSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.data == data
