from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Thing, ThingMessage, Section, Deal
from comments.serializers import CommentSerializer
from tags.serializers import TagSerializer
from tags.models import Tag
from django.contrib.auth.models import User
from things.services.deal import update_deal


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


class CreateThingSerializer(serializers.Serializer):
    title = serializers.CharField()
    state = serializers.ChoiceField(choices=Thing.STATE_CHOICES)
    owner = serializers.CharField()
    content = serializers.CharField()
    section = serializers.CharField()
    tags = serializers.CharField()

    def validate_tags(self, value):
        tags = value.split(",")
        tags_from_db = Tag.objects.filter(title__in=tags).all()

        if len(tags) != len(tags_from_db):
            raise ValidationError("Не все теги существуют!")
        return list(tags_from_db)

    def validate_section(self, value):
        section = Section.objects.filter(title=value).last()
        if not section:
            raise ValidationError("Такого раздела не существует")
        return section

    def validate_owner(self, value):
        user = User.objects.filter(username=value).last()
        if not user:
            raise ValidationError("Такого пользователя не существует")
        return user


class DateSerializer(serializers.Serializer):
    date_published__gte = serializers.DateField(required=False, source="date")
    owner_id = serializers.IntegerField(required=False, source="owner")


class DealModelSerializer(serializers.ModelSerializer):
    old_owner_name = serializers.StringRelatedField(many=False, source="old_owner")
    new_owner_name = serializers.StringRelatedField(many=False, source="new_owner")

    class Meta:
        model = Deal
        fields = (
            "id",
            "status",
            "created_at",
            "old_owner",
            "old_owner_name",
            "new_owner",
            "new_owner_name",
            "cost",
        )


class CreateDealSerializer(serializers.Serializer):
    cost = serializers.DecimalField(max_digits=6, decimal_places=2)
    thing = serializers.CharField()

    def validate_thing(self, value):
        thing = Thing.objects.filter(id=value).last()
        if not thing:
            raise ValidationError("Вещи с таким id не существует!")
        return thing


class UpdateDealSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["confirmed", "completed"])
    cost = serializers.DecimalField(max_digits=6, decimal_places=2)
    updated_at = serializers.DateTimeField(read_only = True)

    def update(self, instance, validated_data):
        deal = update_deal(instance, **validated_data)
        return deal
