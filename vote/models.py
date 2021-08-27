from django.db import models
from django.contrib.auth.models import User
from things.models import Thing


class Vote(models.Model):
    class ValueChoices(models.IntegerChoices):
        LIKE = 1, "like"
        DISLIKE = -1, "dislike"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    value = models.IntegerField(verbose_name="Статус оценивания", choices=ValueChoices.choices)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        unique_together = ("user", "thing")