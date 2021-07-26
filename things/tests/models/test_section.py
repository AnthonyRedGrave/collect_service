from things.models import Section
import pytest
from things.tests.factories import SectionFactory

pytestmark = pytest.mark.django_db


def test_soft_delete__success():
    count_b_add = Section.objects.count()
    section = SectionFactory()
    section.delete()
    count_a_delete = Section.objects.count()
    assert count_b_add + 1 == count_a_delete
    section.refresh_from_db()
    assert section.deleted == True


def test_hard_delete__success():
    count_before_add = Section.objects.count()
    section = SectionFactory()
    section.delete(True)
    count_after_delete = Section.objects.count()
    assert count_before_add == count_after_delete
