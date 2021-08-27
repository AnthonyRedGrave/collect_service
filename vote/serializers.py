from rest_framework import serializers
from .models import Vote
import logging

logger = logging.getLogger(__name__)


class VoteSerializer(serializers.Serializer):
    user = serializers.CharField(required = False)
    thing = serializers.CharField(required = False)
    value = serializers.ChoiceField(choices=Vote.ValueChoices.labels)

    def to_representation(self, dictionary):
        data = super().to_representation(dictionary)
        if data['value'] == Vote.ValueChoices.LIKE.value:
            data['value'] = Vote.ValueChoices.LIKE.label
            return data
        data['value'] = Vote.ValueChoices.DISLIKE.label
        return data

    def validate_value(self, value):
        if value == Vote.ValueChoices.LIKE.label:
            return Vote.ValueChoices.LIKE.value
        value = Vote.ValueChoices.DISLIKE.value
        return value