from rest_framework.exceptions import APIException
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.response import Response

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer


class MessageViewSet(mixins.CreateModelMixin, ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        chat = serializer.validated_data['chat']
        user = self.request.user
        print(user)
        print(chat.member_1)
        print(chat.member_2)

        if user != chat.member_1 and user != chat.member_2:
            raise APIException("Чтобы отправлять сообщения в чат пользователь должен быть его участником!")
        Message.objects.create(**serializer.validated_data, user = self.request.user)
        


class ChatViewSet(ReadOnlyModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]