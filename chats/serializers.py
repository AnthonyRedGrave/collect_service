from logging import Manager
from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import Chat, Message

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
    thing_title = serializers.StringRelatedField(many=False, source="thing")

    class Meta:
        model = Chat
        fields = ('id', 'member_1', 'member_2', 'thing', 'member_1_name', 'member_2_name', 'thing_title')