import csv


import logging
from things.models import Thing
from comments.models import Comment
from things.serializers import CreateThingSerializer


READ_ONLY = "r"

WRITE_ONLY = "w"

DELIMETER_SEMICOLON = ";"

CSV_FOLDER = "media/csv-things/"

logger = logging.getLogger("things.services")


def _get_csv_path(filename):
    return f"{CSV_FOLDER}{filename}"


def thing_row_validate(data_row):
    logger.info("Валидация полей вещи из csv файла", {'row': data_row})
    serializer = CreateThingSerializer(data=data_row)
    serializer.is_valid(raise_exception=True)
    logger.info("Поля из csv файла провалидированы")
    return serializer.validated_data


def thing_save(validated_thing_row, row):
    logger.info("Создание вещи из поля csv файла")
    tags = validated_thing_row.pop("tags")
    thing = Thing.objects.create(**validated_thing_row)
    thing.tags.set(tags)

    if row["comments"]:
        comment_titles = row["comments"].split(",")
        for comment_title in comment_titles:
            Comment.objects.create(
                content=comment_title,
                user=validated_thing_row["owner"],
                content_object=thing,
            )

    thing.save()
    logger.info("Сохранение вещи из csv файла")
    return thing


def csv_import(filename):
    try:
        with open(_get_csv_path(filename), READ_ONLY, encoding="utf-8") as f:
            logger.info("Открытие файла", {'filename': filename})
            fieldnames = [
                "title",
                "content",
                "state",
                "owner",
                "section",
                "tags",
                "comments",
            ]
            reader = csv.DictReader(
                f, fieldnames=fieldnames, delimiter=DELIMETER_SEMICOLON
            )
            for row in reader:
                thing = thing_row_validate(row)
                thing_save(thing, row)
            logger.info("Закрытие файла", {'filename': filename})
    except FileNotFoundError as error:
        logger.error('Файла не существует', {'filename': filename})
        print(error)


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
        return image.url
    return ""


field_managers = {
    "is_sold": _get_is_sold_value,
    "tags": _get_tags_value,
    "comments": _get_comments_value,
    "image": _get_image_url,
}


def _get_thing_field_values(thing, fields):
    logger.info("Запись полей вещи в csv файл")
    field_values = {}
    for field in fields:
        value = getattr(thing, field)
        if field in field_managers.keys():
            value = field_managers[field](value)
            field_values[field] = value
        else:
            field_values[field] = value
    return field_values


def writer(file, things, thing_fields):
    logger.info("Запись вещей в файл")
    fields = ["#"] + thing_fields
    writer = csv.DictWriter(file, delimiter=DELIMETER_SEMICOLON, fieldnames=fields)
    writer.writeheader()
    for row_number, thing in enumerate(things):
        field_values_dict = {"#": row_number}
        field_values_dict.update(_get_thing_field_values(thing, thing_fields))
        writer.writerow(field_values_dict)
    return file


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
    with open(_get_csv_path(filename), WRITE_ONLY, encoding="utf-8") as file:
        logger.info(f"Создание файла для экспорта", {'filename': filename})
        file = writer(file, things, thing_fields)
        return file
