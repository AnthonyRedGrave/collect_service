import pytest

from collect_api.tests.factories import UserFactory, SectionFactory
from pytest_factoryboy import register
from collect_api.serializers import ThingSerializer
from rest_framework.validators import ValidationError

register(UserFactory)
register(SectionFactory)

pytestmark = pytest.mark.django_db

@pytest.mark.parametrize("title, state", [("Монетка", "Awesome"), ("  Фантик  ", "Good"), ("123", "Shabby")])
def test_thing_serializer_title_state__success(title, state):
    user = UserFactory()
    section = SectionFactory()
    data = {
        'title': title, 
        'state': state, 
        'owner': user.id, 
        'content': "Контент для вещи", 
        'section': section.id
    }
    serializer = ThingSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


@pytest.mark.parametrize("title, state", [(None, "Not valid state"), (False, ""), ("", "  Awesome  ")])
def test_thing_serializer_title_state__error(title, state):
    user = UserFactory()
    section = SectionFactory()
    data = {
        'title': title, 
        'state': state, 
        'owner': user.id, 
        'content': "Контент для вещи", 
        'section': section.id
    }
    serializer = ThingSerializer(data=data)

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
    assert 'title' in serializer.errors.keys()
    assert 'state' in serializer.errors.keys()
    assert 'content' not in serializer.errors.keys()
    assert 'section' not in serializer.errors.keys()
    assert 'owner' not in serializer.errors.keys()


@pytest.mark.parametrize("content", ("Content1", "   Content2   ", "12345689"))
def test_thing_serializer_content__success(content):
    user = UserFactory()
    section = SectionFactory()
    data = {
        'title': "Монетка 16-го века",
        'state': "Awesome",
        'owner': user.id, 
        'content': content, 
        'section': section.id
    }
    serializer = ThingSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}

@pytest.mark.parametrize("content", ("", None, False))
def test_thing_serializer_content__error(content):
    user = UserFactory()
    section = SectionFactory()
    data = {
        'title': "Монетка 16-го века",
        'state': "Awesome",
        'owner': user.id, 
        'content': content, 
        'section': section.id
    }
    serializer = ThingSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
    assert 'content' in serializer.errors.keys()
    assert 'title' not in serializer.errors.keys()
    assert 'state' not in serializer.errors.keys()
    assert 'section' not in serializer.errors.keys()
    assert 'owner' not in serializer.errors.keys()