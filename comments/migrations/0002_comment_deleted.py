# Generated by Django 3.2.4 on 2021-07-22 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Удалено ли'),
        ),
    ]
