from rest_framework.exceptions import ValidationError
from things.models import Deal
import logging


logger = logging.getLogger(__name__)


def create_deal(new_owner, cost, thing):
    logger.info("Создание новой сделки")
    if thing.deals.exclude(status="completed").exists():
        logger.error("Пользователь не может создать две действующих сделки!")
        raise ValidationError("Нельзя создать две действующих сделки!")

    if thing.owner == new_owner:
        message = "Вы не можете совершить сделку с самим собой!"
        logger.error(message, {'new_owner': new_owner})
        raise ValidationError(message)

    deal = thing.deals.create(
        old_owner=thing.owner,
        new_owner=new_owner,
        status=Deal.StatusChoices.accepted.value,
        cost=cost,
    )
    deal.save()
    return deal


def update_thing_owner(thing, new_owner):
    logger.info("Смена владельца у вещи", {'old_owner': thing.owner, 'new_owner': new_owner})
    thing.owner = new_owner
    thing.save()


def update_deal(deal, status, cost):
    logger.info("Изменение существующей сделки", {'deal': deal})
    if deal.status == Deal.StatusChoices.completed.value:
        message = "Нельзя изменить совершенную сделку!"
        logger.error(message, {'deal_status': deal.status})
        raise ValidationError(message)
    if status == Deal.StatusChoices.completed.value:
        update_thing_owner(deal.thing, deal.new_owner)
    deal.cost = cost
    deal.status = status
    logger.info("Сохранение вещи")
    deal.save()
    return deal