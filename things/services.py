import csv

from .models import Thing
from django.contrib.auth.models import User
from .models import Thing
from .serializers import ThingSerializer

READ_ONLY = "r"

WRITE_ONLY = "w"

DELIMETER = ";"


def data_validate(row):
    data = {
        "title": row[0],
        "content": row[1],
        "state": row[2],
        "section": row[4],
        "owner": row[3]  # если нет юзера raise except validate_field
        # tags
    }
    serializer = ThingSerializer(data=data)
    print(serializer)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data

def csv_import(filename):

    with open(f"media/csv-things/{filename}", READ_ONLY) as f:
        reader = csv.reader(f, delimiter=DELIMETER)
        for row in reader:
            validated_data = data_validate(row)
            print(validated_data)
            thing = Thing(**validated_data)
            print(thing)


def _get_fields(model):
    field_names = model._meta._forward_fields_map.keys()
    # field_names = ["id", "title","content", "state", "section", "date_published", "image", "is_sold", "owner"]
    return field_names


def _write_thing(thing, fields):
    field_values = []
    for field in fields:
        value = getattr(thing, field)
        if value == "":
            value = "None"
            field_values.append(value)
        elif field == "tags":
            tags = value
            for tag in tags.values_list("title", flat=True):
                field_values.append(tag)
        elif field == "comments":
            comments = value
            for comment in comments.values_list("content", flat=True):
                field_values.append(comment)
        else:
            field_values.append(value)

    return field_values


def csv_export(filename):
    things = Thing.objects.all()
    fields = _get_fields(things.model)

    with open(f"media/csv-things/{filename}", WRITE_ONLY) as f:
        writer = csv.writer(f, delimiter=DELIMETER)
        writer.writerow(fields)
        for thing in things:
            field_values = _write_thing(thing, fields)
            writer.writerow(field_values)
