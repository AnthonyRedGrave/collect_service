import csv
from .models import Thing


def csv_export_service(filename = "export.csv"):
    queryset = Thing.objects.all()
    model = queryset.model
    opts = model._meta.fields + model._meta.many_to_many

    with open(f"media/csv-things/{filename}", "w") as f:
        writer = csv.writer(f, delimiter=";")
        field_names = [field.name for field in opts]
        object_fields = ["id", "title","content", "state", "section", "date_published", "image", "is_sold", "owner"]
        writer.writerow(field_names)
        for obj in queryset:
            fields_list = [getattr(obj, field) for field in object_fields]
            fields_list.append(list(obj.tags.values_list("title", flat=True)))
            writer.writerow(fields_list)