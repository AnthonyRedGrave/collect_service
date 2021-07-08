from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import ThingMessage, Thing, Section
from .serializers import SectionSerializer, ThingSerializer, ThingMessageSerializer
from rest_framework.permissions import *

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

class ThingViewSet(ReadOnlyModelViewSet):
    queryset = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = [IsAuthenticated]

    def create(self):
        pass

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

