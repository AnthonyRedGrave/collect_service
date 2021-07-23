from django.db import models
from core.mixins import SoftDeleteMixin


class MyModel(SoftDeleteMixin):
    title = models.CharField(max_length=150)