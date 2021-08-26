import logging
from things.models import Like, Dislike
from things.serializers import AssesmentSerializer

logger = logging.getLogger(__name__)

def like_create_or_delete(validated_data):
    logger.info("Лайк для вещи", {"thing_id": validated_data['thing']})
    dislike = Dislike.objects.filter(**validated_data).last()
    like = Like.objects.filter(**validated_data).last()
    if not like:
        logger.info("Создание лайка для вещи", {"thing_id": validated_data['thing']})
        Like.objects.create(**validated_data)
        if dislike:
            logger.info("Удаление существующего дизлайка для вещи", {"thing_id": validated_data['thing']})
            dislike.delete()
        return {"Like": "Created!"}
    else:
        logger.info("Удаление лайка для вещи", {"thing_id": validated_data['thing']})
        like.delete()
        return {"Like": "Deleted!"}

def dislike_create_or_delete(validated_data):
    logger.info("Дизлайк для вещи", {"thing_id": validated_data['thing']})
    dislike = Dislike.objects.filter(**validated_data).last()
    like = Like.objects.filter(**validated_data).last()
    if not dislike:
        logger.info("Создание дизлайка для вещи", {"thing_id": validated_data['thing']})
        Dislike.objects.create(**validated_data)
        if like:
            logger.info("Удаление существующего лайка для вещи", {"thing_id": validated_data['thing']})
            like.delete()
        return {"Dislike": "Created!"}
    else:
        logger.info("Удаление дизлайка для вещи", {"thing_id": validated_data['thing']})
        dislike.delete()
        return {"Dislike": "Deleted!"}

def create_assesment(request_data, assesment_type):
    logger.info("Оценивание вещи", {"thing_id": request_data['thing']})
    serializer = AssesmentSerializer(data = request_data)
    serializer.is_valid(raise_exception=True)
    if assesment_type == "like":
        responce = like_create_or_delete(serializer.validated_data) 
    else:
        responce = dislike_create_or_delete(serializer.validated_data) 
    return responce