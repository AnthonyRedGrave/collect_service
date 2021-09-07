import pytest
from things.serializers import TagSerializer
from rest_framework.validators import ValidationError


pytestmark = pytest.mark.django_db

@pytest.mark.parametrize("title", ("Монетки", "накЛеЙки", "   title   ", 123))
def test_tag_serializer_title__success(title):
    data = {
        'title': title
    }
    serializer = TagSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.data == {'title': str(title).strip()}
    assert serializer.errors == {}


@pytest.mark.parametrize("title", (False, None, ""))
def test_tag_serializer_title__error(title):
    data = {
        'title': title
    }
    serializer = TagSerializer(data=data)
    with pytest.raises(ValidationError) as e:
        serializer.is_valid(raise_exception = True)
    assert 'title' in serializer.errors.keys()