# Generated by Django 3.2.4 on 2021-07-12 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
        ('things', '0007_alter_thing_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='thing',
            name='tags',
            field=models.ManyToManyField(to='tags.Tag', verbose_name='Тэги к вещи'),
        ),
    ]
