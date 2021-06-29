from django.db import models
from django.contrib.auth.models import User

class Thing(models.Model):
    title = models.CharField('Название вещи', max_length=150)
    content = models.TextField('Описание')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вещь'
        verbose_name_plural = 'Вещи'
           