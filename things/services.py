import csv
from .models import Thing


def csv_export_service(filename = "export.csv"):
    queryset = Thing.objects.all()
    model = queryset.model
    opts = model._meta.fields + model._meta.many_to_many

    with open(f"media/csv-things/{filename}", "w") as f:
        writer = csv.writer(f, delimiter=";")
        field_names = [field.name for field in opts] # здесь все названия полей
        # object_fields = ["id", "title","content", "state", "section", "date_published", "image", "is_sold", "owner"]
        writer.writerow(field_names)
        for obj in queryset:
            field_values = []
            tags = []
            for field in field_names:
                value = getattr(obj, field)
                if value == '':
                    value = 'None'
                if field == 'tags':
                    value = list(value.values_list("title", flat=True)) # если field это теги, значит в value хранится queryset
                field_values.append(value)
            writer.writerow(field_values)
            # fields_list = [getattr(obj, field) for field in object_fields]
            # fields_list.append(list(obj.tags.values_list("title", flat=True)))
            