from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import ThingMessage, Thing, Section
from .serializers import SectionSerializer, ThingSerializer, ThingMessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

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

    @action(detail=True, methods=['get', 'post'])
    def message(self, request, pk=None):
        thing = self.get_object()
        serializer = self.get_serializer(thing, many=False)
        if request.method == "POST":
            ThingMessage.objects.create(content = request.data['content'],
            user=request.user,
            thing = thing)
            return Response({"Thing_message": "Created!"})
        else:
            print(thing.get_messages)
        return Response(serializer.data['get_messages'])

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

