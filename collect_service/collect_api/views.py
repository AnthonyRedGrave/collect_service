from django.db.models import query
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from .models import ThingMessage, Thing, Section
from .serializers import SectionSerializer, ThingSerializer, ThingMessageSerializer
from rest_framework.permissions import *

class ThingMessageViewSet(ModelViewSet):
    queryset = ThingMessage.objects.all()
    serializer_class = ThingMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(self.request.user)
        queryset = ThingMessage.objects.filter(user = self.request.user)
        return queryset


class ThingViewSet(ModelViewSet):
    queryset = Thing.objects.all()
    serializer_class = ThingSerializer


class SectionApiView(ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

