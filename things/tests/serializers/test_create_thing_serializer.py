import pytest

from things.tests.factories import ThingFactory
from things.serializers import CreateThingSerializer
from rest_framework.validators import ValidationError


pytestmark = pytest.mark.django_db

@pytest.mark.parametrize("title", ("Монетка", "  Фантик  ", "мОНетКа", 123))
def test_create_thing_serializer_title__success(title):
    thing = ThingFactory()
    data = {
        'title': title, 
        'state': thing.state, 
        'owner': thing.owner.id, 
        'content': thing.content, 
        'section': thing.section.id
    }
    serializer = CreateThingSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.data == {
                                'title': str(title).strip(), 
                                'state': thing.state,
                                'owner': thing.owner.id, 
                                'image': None,
                                'content': thing.content, 
                                'section': thing.section.id,
                              }
    assert serializer.errors == {}


@pytest.mark.parametrize("state", ("Awesome", "Good", "Shabby"))
def test_create_thing_serializer_state__success(state):
    thing = ThingFactory()
    data = {
        'title': thing.title, 
        'state': state, 
        'owner': thing.owner.id, 
        'content': thing.content, 
        'section': thing.section.id
    }
    serializer = CreateThingSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.data == {
                                'title': thing.title, 
                                'state': state.strip(),
                                'owner': thing.owner.id, 
                                'image': None,
                                'content': thing.content, 
                                'section': thing.section.id,
                              }
    assert serializer.errors == {}


@pytest.mark.parametrize("title", (None, False, ""))
def test_create_thing_serializer_title__error(title):
    thing = ThingFactory()
    data = {
        'title': title, 
        'state': thing.state, 
        'owner': thing.owner.id, 
        'content': thing.content, 
        'section': thing.section.id
    }
    serializer = CreateThingSerializer(data=data)

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
    assert 'title' in serializer.errors.keys()
    assert 'state' not in serializer.errors.keys()
    assert 'content' not in serializer.errors.keys()
    assert 'section' not in serializer.errors.keys()
    assert 'owner' not in serializer.errors.keys()


@pytest.mark.parametrize("state", ("Not valid state", "", "  Awesome  "))
def test_create_thing_serializer_state__error(state):
    thing = ThingFactory()
    data = {
        'title': thing.title, 
        'state': state, 
        'owner': thing.owner.id, 
        'content': thing.content, 
        'section': thing.section.id
    }
    serializer = CreateThingSerializer(data=data)

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
    assert 'state' in serializer.errors.keys()
    assert 'title' not in serializer.errors.keys()
    assert 'content' not in serializer.errors.keys()
    assert 'section' not in serializer.errors.keys()
    assert 'owner' not in serializer.errors.keys()


@pytest.mark.parametrize("content", ("Content1", "   Content2   ", 12345689))
def test_create_thing_serializer_content__success(content):
    thing = ThingFactory()
    data = {
        'title': "Монетка 16-го века",
        'state': "Awesome",
        'owner': thing.owner.id, 
        'content': content, 
        'section': thing.section.id
    }
    serializer = CreateThingSerializer(data=data)
    
    assert serializer.is_valid()
    assert serializer.data == {
                                'title': "Монетка 16-го века",
                                'state': "Awesome",
                                'content': str(content).strip(),
                                'owner': thing.owner.id, 
                                'image': None,
                                'section': thing.section.id,
    }
    assert serializer.errors == {}

@pytest.mark.parametrize("content", ("", None, False))
def test_create_thing_serializer_content__error(content):
    thing = ThingFactory()
    data = {
        'title': "Монетка 16-го века",
        'state': "Awesome",
        'owner': thing.owner.id, 
        'content': content, 
        'section': thing.section.id
    }
    serializer = CreateThingSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
    assert 'content' in serializer.errors.keys()
    assert 'title' not in serializer.errors.keys()
    assert 'state' not in serializer.errors.keys()
    assert 'section' not in serializer.errors.keys()
    assert 'owner' not in serializer.errors.keys()