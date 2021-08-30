from rest_framework import serializers
from .models import Vote
import logging

logger = logging.getLogger(__name__)


class VoteSerializer(serializers.Serializer):
    user = serializers.CharField(required = False)
    thing = serializers.CharField(required = False)
    value = serializers.ChoiceField(choices=Vote.ValueChoices.labels)

    def to_representation(self, dictionary):
        logger.info("VoteSerializer to_representation")
        data = super().to_representation(dictionary)
        votes = {1: "like", -1: "dislike"}
        vote = votes.pop(data['value'])
        data.update({"value":vote})
        return data

    def validate_value(self, value):
        logger.info("Валидация оценки от пользователя", {"value": value})
        votes = {"like": 1, "dislike": -1}
        return votes[value]
