# Generated by Django 3.2.4 on 2021-08-31 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_alter_vote_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='value',
            field=models.IntegerField(choices=[(1, 'like'), (-1, 'dislike')], default=None, null=True, verbose_name='Статус оценивания'),
        ),
    ]
