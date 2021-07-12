from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from .models import Thing, ThingMessage, Section
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from comments.serializers import CommentSerializer



class ThingMessageSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(many=False, source = 'user')
    thing_title = serializers.StringRelatedField(source='thing')
    

    class Meta:
        model = ThingMessage
        fields = ('id', 'user_name', 'thing_title', 'content', 'thing', 'user')


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'title')


class ThingSerializer(serializers.ModelSerializer):
    state = serializers.ChoiceField(choices=Thing.STATE_CHOICES)
    owner_name = serializers.StringRelatedField(many=False, source = 'owner')
    section_name = serializers.StringRelatedField(many=False, source='section')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Thing
        fields = ('id','title', 'state', 'owner_name', 'owner',
                  'content', 'image', 'section',
                  'section_name', 'comments'
                 )
        read_only_fields = ('owner', )