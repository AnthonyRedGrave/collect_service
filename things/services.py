import csv
from tags.models import Tag

from .models import Thing
from django.contrib.auth.models import User
from .models import Thing
from .serializers import CreateThingSerializer

READ_ONLY = "r"

WRITE_ONLY = "w"

DELIMETER_SEMICOLON = ";"
    

def data_validate(row):
    # user__id = user_validate(row[3])
    data = {
        "title": row[0],
        "content": row[1],
        "state": row[2],
        "section": row[4],
        "owner": user__id,  # если нет юзера raise except validate_field
        "tags": row[5],
    }
    serializer = CreateThingSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


def thing_save(validated_data):
    tags = validated_data.pop("tags")
    return Thing.objects.create(**validated_data, tags = tags)
    # thing = Thing.objects.create(
    #     title=validated_data["title"],
    #     state=validated_data["state"],
    #     owner=validated_data["owner"],
    #     content=validated_data["content"],
    #     section=validated_data["section"],
    # )
    # thing.tags.set(**validated_data["tags"])
    # return thing.save()


def csv_import(filename):

    with open(f"media/csv-things/{filename}", READ_ONLY) as f:
        reader = csv.reader(f, delimiter=DELIMETER_SEMICOLON)
        for row in reader:
            validated_data = data_validate(row) # thing = thing row validate
            thing_save(validated_data) # save(thing)


def _get_fields(model):
    field_names = model._meta._forward_fields_map.keys()
    # использовать нижний варик
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
        writer = csv.writer(f, delimiter=DELIMETER_SEMICOLON)
        writer.writerow(fields)
        for thing in things:
            field_values = _write_thing(thing, fields)
            writer.writerow(field_values)
