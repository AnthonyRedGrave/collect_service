from django.db import models
from core.mixins import SoftDeleteMixin

class Tag(SoftDeleteMixin, models.Model):
    title = models.CharField('Название тэга', max_length=150)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('id', 'title')
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'