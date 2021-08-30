import logging

logger = logging.getLogger(__name__)


def get_response(thing, user, value):
    return {'user': user.id,
            'thing': thing.id,
            "value": value}


def create_or_delete_vote(thing, user, value):
    logger.info("Оценивание вещи", {"thing_id": thing.id})
    vote = thing.vote_set.filter(user=user, value=value)
    if vote:
        vote.delete()
        return get_response(thing, user, "Deleted")
    thing.vote_set.filter(user = user).delete()
    thing.vote_set.create(user = user, value = value)
    return get_response(thing, user, value)
