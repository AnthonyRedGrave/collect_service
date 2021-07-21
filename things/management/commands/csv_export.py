from django.core.management.base import BaseCommand
from things.models import Thing
import csv
from django.http import HttpResponse


class Command(BaseCommand):
    help = "CSV-import for thing objects"

    def handle(self, *args, **kwargs):
        queryset = Thing.objects.all()
        model = queryset.model
        opts = model._meta.fields + model._meta.many_to_many

        with open('media/csv-things/export.csv', 'w') as f:
            writer = csv.writer(f, delimiter=";")
            field_names = [field.name for field in opts]
            writer.writerow(field_names)
            for obj in queryset:
                writer.writerow([getattr(obj, field) for field in field_names])
