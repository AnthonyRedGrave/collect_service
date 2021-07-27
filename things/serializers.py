from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Thing, ThingMessage, Section
from comments.serializers import CommentSerializer
from tags.serializers import TagSerializer
from tags.models import Tag


class ThingMessageSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(many=False, source="user")
    thing_title = serializers.StringRelatedField(source="thing")

    class Meta:
        model = ThingMessage
        fields = ("id", "user_name", "thing_title", "content", "thing", "user")


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ("id", "title")


class ThingSerializer(serializers.ModelSerializer):
    state = serializers.ChoiceField(choices=Thing.STATE_CHOICES)
    owner_name = serializers.StringRelatedField(many=False, source="owner")
    section_name = serializers.StringRelatedField(many=False, source="section")
    comments = CommentSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Thing
        fields = (
            "id",
            "title",
            "state",
            "date_published",
            "owner_name",
            "owner",
            "content",
            "image",
            "section",
            "section_name",
            "comments",
            "tags",
        )
        read_only_fields = ("owner",)


class CreateThingSerializer(serializers.ModelSerializer):

    def validate_tags(self, value):
        tags = value.split(",")
        tags_from_db = Tag.objects.filter(title__in = tags).all()
        if len(tags) != len(tags_from_db):
            raise ValidationError("Не все теги существуют!")
        return list(tags_from_db)

    
    def validate_user(self, attrs):
        return super().validate(attrs)


    class Meta:
        model = Thing
        fields = (
            "id",
            "title",
            "state",
            "date_published",
            "owner",
            "content",
            "image",
            "section",
            "comments",
            "tags",
        )


class DateSerializer(serializers.Serializer):
    date_published__gte = serializers.DateField(required=False, source="date")
    owner_id = serializers.IntegerField(required=False, source="owner")
