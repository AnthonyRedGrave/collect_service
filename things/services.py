import csv
from tags.models import Tag

from .models import Thing
from django.contrib.auth.models import User
from .models import Thing
from .serializers import CreateThingSerializer

READ_ONLY = "r"

WRITE_ONLY = "w"

DELIMETER = ";"


def _get_tags(row_tag_titles):
    tags = []
    for title in row_tag_titles:
        tags.append(Tag.objects.get(title=title).id)
    return tags


def data_validate(row):
    tags = _get_tags(row[5].split(","))
    data = {
        "title": row[0],
        "content": row[1],
        "state": row[2],
        "section": row[4],
        "owner": row[3],  # если нет юзера raise except validate_field
        "tags": tags,
    }
    serializer = CreateThingSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


def thing_save(validated_data):
    thing = Thing.objects.create(
        title=validated_data["title"],
        state=validated_data["state"],
        owner=validated_data["owner"],
        content=validated_data["content"],
        section=validated_data["section"],
    )
    thing.tags.set(validated_data["tags"])
    thing.save()


def csv_import(filename):

    with open(f"media/csv-things/{filename}", READ_ONLY) as f:
        reader = csv.reader(f, delimiter=DELIMETER)
        for row in reader:
            validated_data = data_validate(row)
            thing_save(validated_data)


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
