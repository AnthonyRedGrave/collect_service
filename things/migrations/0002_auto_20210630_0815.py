# Generated by Django 3.2.4 on 2021-06-30 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('things', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Названии раздела')),
            ],
            options={
                'verbose_name': 'Раздел',
                'verbose_name_plural': 'Разделы',
            },
        ),
        migrations.AddField(
            model_name='thing',
            name='date_published',
            field=models.DateField(auto_now=True, verbose_name='Дата выставления'),
        ),
        migrations.AddField(
            model_name='thing',
            name='is_sold',
            field=models.BooleanField(default=False, verbose_name='Продано ли'),
        ),
        migrations.AddField(
            model_name='thing',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
        migrations.AddField(
            model_name='thing',
            name='state',
            field=models.CharField(choices=[('Awesome', 'Лучшее'), ('Good', 'Хорошее'), ('Shabby', 'Потрепанное'), ('Bad', 'Плохое')], default=None, max_length=30, verbose_name='Состояние вещи'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='thing',
            name='section',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='things', to='things.section', verbose_name='Раздел'),
            preserve_default=False,
        ),
    ]
