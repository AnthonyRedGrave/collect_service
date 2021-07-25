from django.core.management.base import BaseCommand
from things.services import csv_import_service 

class Command(BaseCommand):
    help = 'CSV-import for thing objects'

    def handle(self, *args, **kwargs):
        csv_import_service()