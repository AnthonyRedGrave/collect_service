from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from .models import Thing, ThingMessage, Section
from django.http import JsonResponse



class ThingMessageSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(many=False, source = 'user')
    thing_title = serializers.StringRelatedField(source='thing')
    

    class Meta:
        model = ThingMessage
        fields = ('id', 'user_name', 'thing_title', 'content', 'user', 'thing')


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'title')


class ThingSerializer(serializers.ModelSerializer):
    state = serializers.ChoiceField(choices=Thing.STATE_CHOICES)
    owner_name = serializers.StringRelatedField(many=False, source = 'owner')
    section_name = serializers.StringRelatedField(many=False, source='section')
    get_messages = serializers.SerializerMethodField()


    def get_messages(self, obj):
        # TODO: избавиться от ответа в json 
        messages = obj.get_messages()
        return JsonResponse(messages, safe=False)

    class Meta:
        model = Thing
        fields = ('id','title', 'state', 'owner_name',
                  'owner', 'content', 'image', 'section',
                  'section_name', 'get_messages')