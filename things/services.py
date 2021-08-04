import csv

from .models import Thing, Deal
from comments.models import Comment
from .serializers import CreateThingSerializer
from datetime import datetime


READ_ONLY = "r"

WRITE_ONLY = "w"

DELIMETER_SEMICOLON = ";"

CSV_FOLDER = "media/csv-things/"

ACCEPTED = Deal.StatusChoices.accepted.value

CONFIRMED = Deal.StatusChoices.confirmed.value

COMPLETED = Deal.StatusChoices.completed.value


def _change_or_create_deal(deal_data):
    status_log = deal_data.pop("status_log", None)
    deal, created = Deal.objects.get_or_create(**deal_data)
    deal.status_log.append(status_log)
    deal.save()
    if status_log['status'] == COMPLETED:
        deal.thing.owner = deal_data['new_owner']
        deal.thing.save()
    return status_log


def _get_deal_data(thing_to_buy, new_owner, status):
    status_log = {
        "status": status,
        "date": f"{datetime.now()}",
        "old_owner": thing_to_buy.owner.username,
        "new_owner": new_owner.username,
        "cost": f"{thing_to_buy.price}",
    }
    deal_data = {
        "old_owner": thing_to_buy.owner,
        "new_owner": new_owner,
        "thing": thing_to_buy,
        "status_log": status_log,
        "cost": f"{thing_to_buy.price}",
    }
    return deal_data


def buy(thing_to_buy, new_owner, status):
    deal_data = _get_deal_data(thing_to_buy, new_owner, status)
    status_log = _change_or_create_deal(deal_data)
    return status_log


# def buy_confirmed(thing_to_buy, new_owner):
#     deal_data = _get_deal_data(thing_to_buy, new_owner, CONFIRMED)
#     status_log = _change_or_create_deal(deal_data)
#     return status_log


# def buy_completed(thing_to_buy, new_owner):
#     deal_data = _get_deal_data(thing_to_buy, new_owner, COMPLETED)
#     status_log = _change_or_create_deal(deal_data)
#     return status_log


def thing_row_validate(data_row):
    serializer = CreateThingSerializer(data=data_row)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


def thing_save(validated_thing_row, row):
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
    return thing


def csv_import(filename):
    try:
        with open(f"{CSV_FOLDER}{filename}", READ_ONLY, encoding="utf-8") as f:
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
    except FileNotFoundError as error:
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
    field_values = {}
    for field in fields:
        value = getattr(thing, field)
        if field in field_managers.keys():
            value = field_managers[field](value)
            field_values[field] = value
        else:
            field_values[field] = value
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

    with open(f"{CSV_FOLDER}{filename}", WRITE_ONLY, encoding="utf-8") as f:
        fields = ["#"] + thing_fields
        writer = csv.DictWriter(f, delimiter=DELIMETER_SEMICOLON, fieldnames=fields)
        writer.writeheader()
        for i, thing in enumerate(things):
            field_values_dict = {"#": i}
            field_values_dict.update(_get_thing_field_values(thing, thing_fields))
            writer.writerow(field_values_dict)
