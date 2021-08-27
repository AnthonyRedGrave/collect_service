import logging

logger = logging.getLogger(__name__)

def create_vote(thing, user, value):
    logger.info("Оценивание вещи", {"thing_id": thing.id})
    thing.vote_set.filter(user = user).delete()
    return thing.vote_set.create(user = user, value = value)
