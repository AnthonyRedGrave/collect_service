import csv

from rest_framework import fields
from .models import Thing
from django.contrib.auth.models import User
from .models import Section, Thing
from .serializers import ThingSerializer

READ_ONLY = "r"

def csv_import_service(filename):
    
    with open(f"media/csv-things/{filename}", "r") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            data = {
                "title": row[0],
                "content": row[1],
                "state": row[2],
                "section": row[4],
                "owner": row[3] # если нет юзера raise except validate_field
                # tags
            }
            serializer = ThingSerializer(data=data)
            print(serializer)
            serializer.is_valid(raise_exception=True)
            print(serializer.validated_data)
            thing = Thing(**serializer.validated_data)
            print(thing)

def _get_fields(model):
    opts = model._meta.fields + model._meta.many_to_many
    field_names = [field.name for field in opts]
    # field_names = ["id", "title","content", "state", "section", "date_published", "image", "is_sold", "owner"]
    return field_names

def _write_thing(thing):
    #сам напишу
    pass

def csv_export_service(filename):
    queryset = Thing.objects.all()
    model = queryset.model
    fields = _get_fields(model)

    with open(f"media/csv-things/{filename}", "w") as f:
        writer = csv.writer(f, delimiter=";")
        
        writer.writerow(fields)
        for obj in queryset:
            field_values = []
            tags = []
            for field in fields:
                value = getattr(obj, field)
                if value == "":
                    value = "None"
                if field == "tags":
                    value = list(
                        value.values_list("title", flat=True)
                    )  # если field это теги, значит в value хранится queryset
                field_values.append(*value)
            writer.writerow(field_values)
