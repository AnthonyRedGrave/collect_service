import csv
from .models import Thing
from django.contrib.auth.models import User
from .models import Section, Thing
from .serializers import ThingSerializer


def csv_import_service(filename="import.csv"):
        with open(f"media/csv-things/{filename}", "r") as f:
            reader = csv.reader(f, delimiter=";")
            for row in reader:
                print(row)
                user = User.objects.get(id=row[3])
                data = {
                    "title": row[0],
                    "content": row[1],
                    "state": row[2],
                    "owner": user.id,
                    "section": row[4],
                }
                serializer = ThingSerializer(data=data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                print(serializer.validated_data)
                thing = Thing(**serializer.validated_data)
                print(thing)


def csv_export_service(filename="export.csv"):
    queryset = Thing.objects.all()
    model = queryset.model
    opts = model._meta.fields + model._meta.many_to_many

    with open(f"media/csv-things/{filename}", "w") as f:
        writer = csv.writer(f, delimiter=";")
        field_names = [field.name for field in opts]  # здесь все названия полей
        # object_fields = ["id", "title","content", "state", "section", "date_published", "image", "is_sold", "owner"]
        writer.writerow(field_names)
        for obj in queryset:
            field_values = []
            tags = []
            for field in field_names:
                value = getattr(obj, field)
                if value == "":
                    value = "None"
                if field == "tags":
                    value = list(
                        value.values_list("title", flat=True)
                    )  # если field это теги, значит в value хранится queryset
                field_values.append(value)
            writer.writerow(field_values)
