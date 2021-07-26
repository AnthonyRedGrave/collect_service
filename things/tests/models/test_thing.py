from things.models import Thing
import pytest
from things.tests.factories import ThingFactory

pytestmark = pytest.mark.django_db


def test_soft_delete__success():
    count_b_add = Thing.objects.count()
    thing = ThingFactory()
    thing.delete()
    count_a_delete = Thing.objects.count()
    assert count_b_add + 1 == count_a_delete
    thing.refresh_from_db()
    assert thing.deleted == True


def test_hard_delete__success():
    count_before_add = Thing.objects.count()
    thing = ThingFactory()
    thing.delete(True)
    count_after_delete = Thing.objects.count()
    assert count_before_add == count_after_delete
