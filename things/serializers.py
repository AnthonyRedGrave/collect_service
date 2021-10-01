from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Thing, ThingMessage, Section, Deal
from comments.serializers import CommentSerializer
from tags.serializers import TagSerializer
from tags.models import Tag
from django.contrib.auth.models import User
from things.services.deal import update_deal
import logging

logger = logging.getLogger(__name__)

class ThingMessageSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(many=False, source="user")
    thing_title = serializers.StringRelatedField(source="thing")

    def validate_user(self, value):
        thing = Thing.objects.filter(id = self.initial_data['thing']).last()
        if value == thing.owner:
            raise ValidationError("Пользователь не может связаться сам с собой!")
        return value
    
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


class PartialUpdateSerializer(serializers.Serializer):
    title = serializers.CharField()
    # state = serializers.ChoiceField(choices=Thing.STATE_CHOICES)
    content = serializers.CharField()
    section = serializers.CharField()
    tags = serializers.CharField()

    def validate_section(self, value):
        section = Section.objects.filter(id=value).last()
        if not section:
            message = "Такого раздела не существует"
            logger.error(message, {'section_id': value})
            raise ValidationError(message)
        return section


    def validate_tags(self, value):
        tags = value.split(",")
        tags_from_db = Tag.objects.filter(id__in=tags).all()
        if len(tags) != len(tags_from_db):
            message = "Не все теги существуют!"
            logger.error(message, {'tags': value})
            raise ValidationError(message)
        return list(tags_from_db)



class CreateThingSerializer(serializers.Serializer):
    title = serializers.CharField()
    state = serializers.ChoiceField(choices=Thing.STATE_CHOICES)
    owner = serializers.CharField()
    content = serializers.CharField()
    section = serializers.CharField()
    tags = serializers.CharField()

    def validate_tags(self, value):
        logger.info("Валидация тегов для создания вещи", {'tags': value})
        tags = value.split(",")
        tags_from_db = Tag.objects.filter(title__in=tags).all()

        if len(tags) != len(tags_from_db):
            message = "Не все теги существуют!"
            logger.error(message, {'tags': value})
            raise ValidationError(message)
        return list(tags_from_db)

    def validate_section(self, value):
        logger.info("Валидация раздела для создания вещи", {'section_id': value})
        section = Section.objects.filter(title=value).last()
        if not section:
            message = "Такого раздела не существует"
            logger.error(message, {'section_id': value})
            raise ValidationError(message)
        return section

    def validate_owner(self, value):
        logger.info("Валидация пользователя для создания вещи", {'owner_id': value})
        user = User.objects.filter(username=value).last()
        if not user:
            message = "Такого пользователя не существует"
            logger.error(message, {'owner_id': value})
            raise ValidationError(message)
        return user


class DateAndOrderingSerializer(serializers.Serializer):
    date_published__gte = serializers.DateField(required=False, source="date")
    owner_id = serializers.IntegerField(required=False, source="owner")
    ordering = serializers.CharField(required=False)

    def validate_ordering(self, value):
        if value not in ['title', '-title']:
            raise ValidationError({"ordering": "Неправильный title для сортировки"})
        return value


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
        logger.info("Валидация вещи для сделки", {'thing_id': value})
        thing = Thing.objects.filter(id=value).last()
        if not thing:
            message = "Вещи с таким id не существует!"
            logger.error(message, {'thing_id': value})
            raise ValidationError(message)
        return thing


class UpdateDealSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["confirmed", "completed"])
    cost = serializers.DecimalField(max_digits=6, decimal_places=2)
    updated_at = serializers.DateTimeField(read_only = True)

    def update(self, instance, validated_data):
        logger.info("update записи в UpdateDealSerializer", {'deal': instance})
        deal = update_deal(instance, **validated_data)
        return deal

