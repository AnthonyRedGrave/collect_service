from logging import Manager
from rest_framework import serializers
from .models import Chat, Message

class MessageSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(many=False, source="user")
    
    class Meta:
        model = Message
        fields = ('user', 'content', 'chat')


class ChatSerializer(serializers.ModelSerializer):
    member_1_name = serializers.StringRelatedField(many=False, source="member_1")
    member_2_name = serializers.StringRelatedField(many=False, source="member_2")
    thing_title = serializers.StringRelatedField(many=False, source="thing")

    class Meta:
        model = Chat
        fields = ('member_1', 'member_2', 'thing')