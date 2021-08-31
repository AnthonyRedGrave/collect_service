import logging

logger = logging.getLogger(__name__)


def create_or_delete_vote(thing, user, value):
    logger.info("Оценивание вещи", {"thing_id": thing.id})
    vote = thing.vote_set.filter(user=user, value=value).last()
    if vote:
        vote.value = None
        return vote.save()
    thing.vote_set.filter(user = user).delete()
    return thing.vote_set.create(user = user, value = value)
