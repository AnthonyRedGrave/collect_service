from rest_framework.exceptions import ValidationError
from things.models import Deal


def create_deal(new_owner, cost, thing):
    if thing.deals.exclude(status="completed").exists():
        raise ValidationError("Нельзя создать две действующих сделки!")

    if thing.owner == new_owner:
        raise ValidationError("Вы не можете совершить сделку с самим собой!")

    deal = thing.deals.create(
        old_owner=thing.owner,
        new_owner=new_owner,
        status=Deal.StatusChoices.accepted.value,
        cost=cost,
    )
    deal.update_status_log()
    deal.save()
    return deal


def update_thing_owner(thing, new_owner):
    thing.owner = new_owner
    thing.save()


def update_deal(deal, status, cost):
    if deal.status == Deal.StatusChoices.completed.value:
        raise ValidationError("Нельзя изменить совершенную сделку!")
    if status == Deal.StatusChoices.completed.value:
        update_thing_owner(deal.thing, deal.new_owner)
    deal.cost = cost
    deal.status = status
    deal.update_status_log()
    deal.save()
    return deal