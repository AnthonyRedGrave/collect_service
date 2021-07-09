from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import ThingMessage, Thing, Section
from .serializers import SectionSerializer, ThingSerializer, ThingMessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework import status

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
        if request.method == "POST":
            data = {'content': request.data['content'],
                    'user': request.user.id,
                    'thing': thing.id}
            thing_message_serializer = ThingMessageSerializer(data=data)
            if thing_message_serializer.is_valid():
                ThingMessage.objects.create(content = thing_message_serializer.validated_data['content'],
                                            user=thing_message_serializer.validated_data['user'],
                                            thing = thing_message_serializer.validated_data['thing'])
                return Response({"Thing_message": "Created!"})
            else:
                return Response(thing_message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(thing.get_messages, safe=False)

        

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

