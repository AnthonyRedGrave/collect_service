# Generated by Django 3.2.4 on 2021-06-30 08:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('things', '0003_thing_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThingMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Текст сообщения')),
                ('thing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thing_messages', to='things.thing', verbose_name='Вещь, для которой пишется сообщение')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Собщения',
            },
        ),
    ]