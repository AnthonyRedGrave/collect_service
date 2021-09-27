from django.db import models
from things.models import Thing, ThingMessage
from django.contrib.auth.models import User

class Chat(models.Model):
    member_1 = models.ForeignKey(User, verbose_name='Первый участник', on_delete=models.CASCADE, blank=False, related_name='member1_chat')
    member_2 = models.ForeignKey(User, verbose_name='Второй участник', on_delete=models.CASCADE, blank=False, related_name='member2_chat')
    thing = models.ForeignKey(Thing, verbose_name='Вещь обсуждения', on_delete=models.CASCADE, blank=False, related_name='chats')

    def __str__(self):
        return f'Чат {self.member_1} и {self.member_2}'

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Message(models.Model):
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE, blank=False
    )
    content = models.TextField("Текст сообщения")
    chat = models.ForeignKey(Chat, verbose_name='Чат', on_delete=models.CASCADE, related_name='messages', blank=False)

    def __str__(self):
        return f"Сообщение от {self.user}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Собщения"
