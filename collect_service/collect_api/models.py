from django.db import models
from django.contrib.auth.models import User

class ThingMessage(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=False)
    content = models.TextField('Текст сообщения')
    thing = models.ForeignKey('Thing', on_delete=models.CASCADE, related_name='thing_messages', verbose_name='Вещь, для которой пишется сообщение', blank=False)

    def __str__(self):
        return f'Сообщение от {self.user}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Собщения'


class Section(models.Model):
    title = models.CharField('Названии раздела', max_length=150)

    def __str__(self):
        return f'Раздел {self.title}'

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

class Thing(models.Model):

    STATE_CHOICES = [
        ('Awesome', 'Лучшее'),
        ('Good', 'Хорошее'),
        ('Shabby', 'Потрепанное'),
        ('Bad', 'Плохое')
    ]

    title = models.CharField('Название вещи', max_length=150)
    content = models.TextField('Описание')
    state = models.CharField(verbose_name='Состояние вещи', choices=STATE_CHOICES, max_length=50)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name='Раздел', related_name='things', blank=False)
    date_published = models.DateField('Дата выставления', auto_now=True)
    image = models.ImageField('Изображение вещи', null=True, blank=True, upload_to='things/images/')
    is_sold = models.BooleanField('Продано ли', default=False)
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE, blank=False)


    @property
    def get_messages(self): 
        return list(self.thing_messages.values('id','user__username', 'content'))


    def __str__(self):
        return f'Вещь {self.title}'

    class Meta:
        verbose_name = 'Вещь'
        verbose_name_plural = 'Вещи'
           