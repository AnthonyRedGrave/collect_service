import pytest

from things.tests.factories import ThingFactory
from things.serializers import CreateThingSerializer
from rest_framework.validators import ValidationError
from django.contrib.auth.models import User


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("tags", (["1", "2", "3"], [True, False, True], [0, 0, 0]))
def test_create_thing_serializer_tags__error(tags):
    thing = ThingFactory()
    data = {
        "title": thing.title,
        "state": thing.state,
        "owner": thing.owner.id,
        "content": thing.content,
        "section": thing.section.id,
        "tags": tags,
    }
    serializer = CreateThingSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
    assert "tags" in serializer.errors.keys()


@pytest.mark.parametrize("title", ("Монетка", "  Фантик  ", "мОНетКа", 123))
def test_create_thing_serializer_title__success(title):
    thing = ThingFactory(tags=4, owner__username = "admin")
    data = {
        "title": title,
        "state": thing.state,
        "owner": thing.owner.username,
        "content": thing.content,
        "section": thing.section.title,
        "tags": ",".join(list(thing.tags.values_list("title", flat=True))),
    }
    serializer = CreateThingSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.data == {
        "title": str(title).strip(),
        "state": thing.state,
        "owner": thing.owner.username,
        "content": thing.content,
        "section": thing.section.__str__(),
        "tags": f'{list(thing.tags.all())}',
    }
    assert serializer.errors == {}


@pytest.mark.parametrize("state", ("Awesome", "Good", "Shabby"))
def test_create_thing_serializer_state__success(state):
    thing = ThingFactory(tags=4)
    data = {
        "title": thing.title,
        "state": state,
        "owner": thing.owner.username,
        "content": thing.content,
        "section": thing.section.title,
        "tags": ",".join(list(thing.tags.values_list("title", flat=True))),
    }
    serializer = CreateThingSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.data == {
        "title": str(thing.title).strip(),
        "state": str(state).strip(),
        "owner": thing.owner.username,
        "content": thing.content,
        "section": thing.section.__str__(),
        "tags": f'{list(thing.tags.all())}',
    }
    assert serializer.errors == {}


@pytest.mark.parametrize("title", (None, False, ""))
def test_create_thing_serializer_title__error(title):
    thing = ThingFactory(tags=4)
    data = {
        "title": title,
        "state": thing.state,
        "owner": thing.owner.username,
        "content": thing.content,
        "section": thing.section.title,
        "tags": ",".join(list(thing.tags.values_list("title", flat=True))),
    }
    serializer = CreateThingSerializer(data=data)

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
    assert "title" in serializer.errors.keys()
    assert "state" not in serializer.errors.keys()
    assert "content" not in serializer.errors.keys()
    assert "section" not in serializer.errors.keys()
    assert "owner" not in serializer.errors.keys()
    assert "tags" not in serializer.errors.keys()


@pytest.mark.parametrize("state", ("Not valid state", "", "  Awesome  "))
def test_create_thing_serializer_state__error(state):
    thing = ThingFactory(tags=2)
    data = {
        "title": thing.title,
        "state": state,
        "owner": thing.owner.username,
        "content": thing.content,
        "section": thing.section.title,
        "tags": ",".join(list(thing.tags.values_list("title", flat=True))),
    }
    serializer = CreateThingSerializer(data=data)

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
    assert "state" in serializer.errors.keys()
    assert "title" not in serializer.errors.keys()
    assert "content" not in serializer.errors.keys()
    assert "section" not in serializer.errors.keys()
    assert "owner" not in serializer.errors.keys()
    assert "tags" not in serializer.errors.keys()

@pytest.mark.parametrize("content", ("Content1", "   Content2   ", 12345689))
def test_create_thing_serializer_content__success(content):
    thing = ThingFactory(tags=4)
    data = {
        "title": "Монетка 16-го века",
        "state": "Awesome",
        "owner": thing.owner.username,
        "content": content,
        "section": thing.section.title,
        "tags": ",".join(list(thing.tags.values_list("title", flat=True))),
    }
    serializer = CreateThingSerializer(data=data)

    assert serializer.is_valid()
    assert serializer.data == {
        "title": "Монетка 16-го века",
        "state": "Awesome",
        "content": str(content).strip(),
        "owner": thing.owner.username,
        "section": thing.section.__str__(),
        "tags": f'{list(thing.tags.all())}',
    }
    assert serializer.errors == {}


@pytest.mark.parametrize("content", ("", None, False))
def test_create_thing_serializer_content__error(content):
    thing = ThingFactory(tags=4)
    data = {
        "title": "Монетка 16-го века",
        "state": "Awesome",
        "owner": thing.owner.username,
        "content": content,
        "section": thing.section.title,
        "tags": ",".join(list(thing.tags.values_list("title", flat=True))),
    }
    serializer = CreateThingSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
    assert "content" in serializer.errors.keys()
    assert "title" not in serializer.errors.keys()
    assert "state" not in serializer.errors.keys()
    assert "section" not in serializer.errors.keys()
    assert "owner" not in serializer.errors.keys()
    assert "tags" not in serializer.errors.keys()


@pytest.mark.parametrize("owner", ("1", "wrong_user", 0))
def test_create_thing_serializer_owner__error(owner):
    thing = ThingFactory(tags=2)
    data = {
        "title": thing.title,
        "state": thing.state,
        "owner": owner,
        "content": thing.content,
        "section": thing.section.title,
        "tags": ",".join(list(thing.tags.values_list("title", flat=True))),
    }
    serializer = CreateThingSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
    assert "owner" in serializer.errors.keys()
    assert "content" not in serializer.errors.keys()
    assert "title" not in serializer.errors.keys()
    assert "state" not in serializer.errors.keys()
    assert "section" not in serializer.errors.keys()
    assert "tags" not in serializer.errors.keys()