import pytest
from rest_framework import serializers
from collect_api.tests.factories import SectionFactory
from pytest_factoryboy import register
from collect_api.serializers import SectionSerializer
from rest_framework.validators import ValidationError

register(SectionFactory)

pytestmark = pytest.mark.django_db

# @pytest.mark.parametrize("title", [("Монетки"), ("Фантики")])
# def test_section_serializer__success(title):
#     data = {
#         'title': title
#     }
#     serializer = SectionSerializer(data=data)
#     assert serializer.is_valid()
#     assert serializer.data == data


@pytest.mark.parametrize("title", (False, 123, None))
def test_section_serializer__error(title):
    section = SectionFactory()
    data = {
        'title': section.title
    }
    print(title)
    serializer = SectionSerializer(data=data)
    with pytest.raises(ValidationError) as e:
        serializer.is_valid(raise_exception = True)