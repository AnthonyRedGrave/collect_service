from django.core.management.base import BaseCommand
from things.models import Thing
import csv


class Command(BaseCommand):
    help = "CSV-import for thing objects"

    def handle(self, *args, **kwargs):
        pass