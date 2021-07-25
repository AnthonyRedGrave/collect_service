from django.core.management.base import BaseCommand
from things.models import Thing
from thing.services import csv_export_service
import csv


class Command(BaseCommand):
    help = "CSV-import for thing objects"

    def handle(self, *args, **kwargs):
        csv_export_service()