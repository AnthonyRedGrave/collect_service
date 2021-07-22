from django.core.management.base import BaseCommand
from things.models import Section, Thing
from django.contrib.auth.models import User
import csv 

class Command(BaseCommand):
    help = 'CSV-import for thing objects'

    def handle(self, *args, **kwargs):
        with open('media/csv-things/import.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                user = User.objects.get(id=row[3])
                section, _ = Section.objects.get_or_create(title=row[4])
                Thing.objects.create(title=row[0], content=row[1], state=row[2], owner=user, section=section)