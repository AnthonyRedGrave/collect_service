from tags.models import Tag
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comment
from core.mixins import SoftDeleteMixin


class Section(SoftDeleteMixin, models.Model):
    title = models.CharField("Названии раздела", max_length=150)

    def __str__(self):
        return f"Раздел {self.title}"

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"


class Thing(SoftDeleteMixin, models.Model):

    STATE_CHOICES = [
        ("Awesome", "Лучшее"),
        ("Good", "Хорошее"),
        ("Shabby", "Потрепанное"),
        ("Bad", "Плохое"),
    ]

    title = models.CharField("Название вещи", max_length=150)
    content = models.TextField("Описание")
    state = models.CharField(
        verbose_name="Состояние вещи", choices=STATE_CHOICES, max_length=50
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,
        verbose_name="Раздел",
        related_name="things",
        blank=False,
    )
    date_published = models.DateField("Дата выставления", auto_now=True)
    image = models.ImageField(
        "Изображение вещи", null=True, blank=True, upload_to="things/images/"
    )
    is_sold = models.BooleanField("Продано ли", default=False)
    owner = models.ForeignKey(
        User, verbose_name="Владелец", on_delete=models.CASCADE, blank=False
    )
    comments = GenericRelation(Comment)
    tags = models.ManyToManyField(Tag, verbose_name="Тэги к вещи")
    price = models.DecimalField(verbose_name="Цена вещи", default=0, decimal_places=2, max_digits=6)

    def get_comments(self):
        return self.comments.all()

    def __str__(self):
        return f"Вещь {self.title}"

    class Meta:
        verbose_name = "Вещь"
        verbose_name_plural = "Вещи"
        ordering = ["-date_published"]


class ThingMessage(SoftDeleteMixin, models.Model):
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE, blank=False
    )
    content = models.TextField("Текст сообщения")
    thing = models.ForeignKey(
        Thing,
        on_delete=models.CASCADE,
        related_name="thing_messages",
        verbose_name="Вещь, для которой пишется сообщение",
        blank=False,
    )

    def __str__(self):
        return f"Сообщение от {self.user}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Собщения"


class Transaction(models.Model):

    STATUS_TYPES = [
        ("Accepted", "Принят"),
        ("Confirmed", "Подтвержден"),
        ("Completed", "Выполнен"),
    ]

    owner = models.ForeignKey(
        User,
        verbose_name="Владелец вещи",
        on_delete=models.CASCADE,
        blank=False,
        related_name="own_thing_transcation",
    )
    customer = models.ForeignKey(
        User,
        verbose_name="Покупатель",
        on_delete=models.CASCADE,
        blank=False,
        related_name="buy_thing_transcation",
    )
    thing = models.ForeignKey(
        Thing,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="Вещь, для которой пишется сообщение",
        blank=False,
    )
    status = models.CharField(verbose_name="Статус заказа", choices=STATUS_TYPES, max_length=15)
    date_deal = models.DateTimeField(auto_now=True, verbose_name="Дата и время сделки")
    cost = models.DecimalField(
        verbose_name="Цена сделки", max_digits=6, decimal_places=2, null=True
    )
    status_log = models.JSONField()


    def __str__(self):
        return f"Сделка между {self.owner} и {self.customer}"

    class Meta:
        verbose_name = "Сделка"
        verbose_name = "Сделки"
