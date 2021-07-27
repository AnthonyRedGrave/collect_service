import csv

from .models import Thing
from comments.models import Comment
from .serializers import CreateThingSerializer

READ_ONLY = "r"

WRITE_ONLY = "w"

DELIMETER_SEMICOLON = ";"


def thing_row_validate(row):

    data = {
        "title": row[0],
        "content": row[1],
        "state": row[2],
        "section": row[4],
        "owner": row[3],
        "tags": row[5],
    }
    serializer = CreateThingSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


def thing_save(validated_thing_row, row):
    tags = validated_thing_row.pop("tags")
    comment_titles = row[6].split(",")

    thing = Thing.objects.create(**validated_thing_row)
    thing.tags.set(tags)

    for comment_title in comment_titles:
        Comment.objects.create(
            content=comment_title,
            user=validated_thing_row["owner"],
            content_object=thing,
        )

    thing.save()
    return thing


def csv_import(filename):
    with open(f"media/csv-things/{filename}", READ_ONLY, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=DELIMETER_SEMICOLON)
        for row in reader:
            thing = thing_row_validate(row)
            thing_save(thing, row)


def _get_tags_value(tags):
    return ";".join(tags.values_list("title", flat=True))


def _get_comments_value(comments):
    return ";".join(comments.values_list("content", flat=True))


def _get_is_sold_value(is_sold):
    if is_sold:
        return "Sold"
    return "Not sold"


def _get_image_url(image):
    if image:
        # не доделал
        return image.url
    return ""


field_managers = {
    "is_sold": _get_is_sold_value,
    "tags": _get_tags_value,
    "comments": _get_comments_value,
    "image": _get_image_url,
}


def _get_thing_field_values(thing, fields):
    field_values = []
    for field in fields:
        value = getattr(thing, field)
        if field in field_managers.keys():
            value = field_managers[field](value)
            field_values.append(value)
        else:
            field_values.append(value)
    return field_values


def csv_export(filename):
    things = Thing.objects.all()
    thing_fields = [
        "title",
        "content",
        "state",
        "section",
        "date_published",
        "image",
        "is_sold",
        "owner",
        "tags",
        "comments",
    ]

    with open(f"media/csv-things/{filename}", WRITE_ONLY, encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=DELIMETER_SEMICOLON)
        fields = ["#"] + thing_fields
        writer.writerow(fields)
        for i, thing in enumerate(things):
            row = [i]
            field_values = _get_thing_field_values(thing, thing_fields)
            row = row + field_values
            writer.writerow(row)
