# Generated by Django 3.2.4 on 2021-08-04 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0016_alter_deal_status_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='status_log',
            field=models.JSONField(default=list),
        ),
    ]
