import logging
from things.models import Assesment
from things.serializers import AssesmentSerializer

logger = logging.getLogger(__name__)

def like_create_or_delete(validated_data):
    logger.info("Лайк для вещи", {"thing_id": validated_data['thing']})
    dislike = Assesment.objects.filter(**validated_data).last()
    like = Assesment.objects.filter(**validated_data).last()
    if not like:
        logger.info("Создание лайка для вещи", {"thing_id": validated_data['thing']})
        Assesment.objects.create(**validated_data)
        if dislike:
            logger.info("Удаление существующего дизлайка для вещи", {"thing_id": validated_data['thing']})
            dislike.delete()
        return {"Like": "Created!"}
    else:
        logger.info("Удаление лайка для вещи", {"thing_id": validated_data['thing']})
        like.delete()
        return {"Like": "Deleted!"}

# def dislike_create_or_delete(validated_data):
#     logger.info("Дизлайк для вещи", {"thing_id": validated_data['thing']})
#     dislike = Assesment.objects.filter(**validated_data).last()
#     like = Assesment.objects.filter(**validated_data).last()
#     if not dislike:
#         logger.info("Создание дизлайка для вещи", {"thing_id": validated_data['thing']})
#         Assesment.objects.create(**validated_data)
#         if like:
#             logger.info("Удаление существующего лайка для вещи", {"thing_id": validated_data['thing']})
#             like.delete()
#         return {"Dislike": "Created!"}
#     else:
#         logger.info("Удаление дизлайка для вещи", {"thing_id": validated_data['thing']})
#         dislike.delete()
#         return {"Dislike": "Deleted!"}

def assesment_create_or_create(validated_data):
    assesment_status = validated_data.pop("type")
    assesment = Assesment.objects.filter(**validated_data, status = assesment_status).last()
    if assesment:
        logger.info("Удаление существующей оценки вещи", {"thing_id": validated_data['thing']})
        assesment.delete()
        return {assesment_status: "Deleted!"}
    else:
        logger.info("Создание оценки вещи", {"thing_id": validated_data['thing']})
        opposite_assesment = Assesment.objects.filter(**validated_data).exclude(status = assesment_status).last()
        if opposite_assesment:
            logger.info("Удаление противоположной оценки вещи", {"thing_id": validated_data['thing']})
            opposite_assesment.delete()
        Assesment.objects.create(**validated_data, status=assesment_status)
        return {assesment_status: "Created!"}

    

def create_assesment(validated_data):
    logger.info("Оценивание вещи", {"thing_id": validated_data['thing']})
    responce = assesment_create_or_create(validated_data) 
    return responce