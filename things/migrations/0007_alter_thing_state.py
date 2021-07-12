# Generated by Django 3.2.4 on 2021-07-12 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0006_alter_thing_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thing',
            name='state',
            field=models.CharField(choices=[('Awesome', 'Лучшее'), ('Good', 'Хорошее'), ('Shabby', 'Потрепанное'), ('Bad', 'Плохое')], max_length=50, verbose_name='Состояние вещи'),
        ),
    ]
