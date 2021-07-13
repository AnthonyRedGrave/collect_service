import pytest
from rest_framework.exceptions import ValidationError
from comments.serializers import CommentSerializer
from things.tests.factories import ThingFactory


pytestmark = pytest.mark.django_db

@pytest.mark.parametrize("content", ("Текст первого комментария", "тЕкСт ПерВОго коМменТаРИЯ", "   Комментарий   ", 123, "<script>alert(1)</script>", "select * from users; word"))
def test_comment_serializer_content__success(content):
    thing = ThingFactory()
    data = {
        'content': content,
        'user': thing.owner.id
    }

    serializer = CommentSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.data == {
                                'content': str(content).strip(),
                                'user_name': thing.owner.username, 
                                'user': thing.owner.id
                              }
    assert serializer.errors == {}



@pytest.mark.parametrize("content", (False, "", None))
def test_comment_serializer_content__error(content):
    thing = ThingFactory()
    data = {
        'content': content,
        'user': thing.owner.id
    }
       
    serializer = CommentSerializer(data=data)
    with pytest.raises(ValidationError) as e:
        serializer.is_valid(raise_exception = True)
    assert 'content' in serializer.errors.keys()
    assert 'user' not in serializer.errors.keys()