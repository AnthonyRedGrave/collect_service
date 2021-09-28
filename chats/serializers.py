from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import Chat, Message
from things.models import Thing

class MessageSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(many=False, source="user")
    chat = serializers.CharField()
    
    class Meta:
        model = Message
        fields = ('id', 'user', 'content', 'chat', 'user_name')
        read_only_fields = ('user', )

    def validate_chat(self, value):
        chat = Chat.objects.filter(id=value).last()
        if not chat:
            raise ValidationError("Такого чата не существует!")
        return chat



class ChatSerializer(serializers.ModelSerializer):
    member_1_name = serializers.StringRelatedField(many=False, source="member_1")
    member_2_name = serializers.StringRelatedField(many=False, source="member_2")
    thing = serializers.CharField()

    class Meta:
        model = Chat
        fields = ('id', 'member_1', 'member_2', 'thing', 'member_1_name', 'member_2_name')

    def validate(self, data):
        member_1 = data['member_1']
        member_2 = data['member_2']
        thing = data['thing']
        if thing.owner != member_1 and thing.owner != member_2:
            raise ValidationError({"thing": "Невозможно создать чат с такими пользователями"})
        return data

    def validate_thing(self, value):
        thing = Thing.objects.filter(id=value).last()
        if not thing:
            raise ValidationError("Такой вещи не существует!")
        return thing