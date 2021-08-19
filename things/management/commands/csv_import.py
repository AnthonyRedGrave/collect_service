from django.core.management.base import BaseCommand
from things.services.csv import csv_import
import logging

logger = logging.getLogger('things.management.commands')

class Command(BaseCommand):
    help = 'CSV-import for thing objects'

    def add_arguments(self, parser):
        parser.add_argument("--f", "--filename",type=str)

    def handle(self, *args, **kwargs):
        filename = kwargs['f']
        logger.info("Импорт записей как management комманда из файла", {'filename': filename})
        csv_import(filename)