from rest_framework.response import Response
from rest_framework.settings import perform_import
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import ThingMessage, Thing, Section
from .serializers import SectionSerializer, ThingSerializer, ThingMessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.core import serializers
from rest_framework import mixins

class ThingMessageViewSet(ReadOnlyModelViewSet):
    queryset = ThingMessage.objects.all()
    serializer_class = ThingMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(user = self.request.user)
        return queryset

    def create(self):
        pass

    def destroy(self):
        pass

    def update(self):
        pass

class ThingViewSet(mixins.CreateModelMixin, ReadOnlyModelViewSet):
    queryset = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = [IsAuthenticated]
    # http_method_names = ['get', 'post', 'head']

    @action(detail=True, methods=['get', 'post'])
    def message(self, request, pk=None):
        thing = self.get_object()
        if request.method == "POST":
            data = {'content': request.data['content'],
                    'user': request.user.id,
                    'thing': thing.id}
            thing_message_serializer = ThingMessageSerializer(data=data)

            thing_message_serializer.is_valid(raise_exception=True)
            ThingMessage.objects.create(**thing_message_serializer.validated_data)
            return Response({"Thing_message": "Created!"})
        else:
            serializer = ThingMessageSerializer(data=thing.get_messages, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)

    def perform_create(self, serializer):
        Thing.objects.create(**serializer.validated_data, owner=self.request.user)


    def destroy(self):
        pass

    def update(self):
        pass

class SectionViewSet(ReadOnlyModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]

    def create(self):
        pass

    def destroy(self):
        pass

    def update(self):
        pass