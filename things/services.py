import csv
from .models import Thing


def csv_export_service(filename):
    queryset = Thing.objects.all()
    model = queryset.model
    opts = model._meta.fields + model._meta.many_to_many

    with open(f"media/csv-things/{filename}", "w") as f:
        writer = csv.writer(f, delimiter=";")
        field_names = [field.name for field in opts]
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
