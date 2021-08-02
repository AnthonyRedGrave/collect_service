from comments.models import Comment
from comments.serializers import CommentSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import ThingMessage, Thing, Section, Transaction
from .serializers import SectionSerializer, ThingSerializer, ThingMessageSerializer, DateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import mixins
from django.db.models import Count


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
    queryset = Thing.objects.all().prefetch_related('tags', 'comments').select_related('owner', 'section')
    serializer_class = ThingSerializer
    permission_classes = [IsAuthenticated]
    # http_method_names = ['get', 'post', 'head']
    #things = Thing.objects.all().prefetch_related('tags').annotate(num_tags=Count('tags'))

    def get_queryset(self):
        queryset = super().get_queryset()
        seriliazer = DateSerializer(data = self.request.query_params)
        seriliazer.is_valid(raise_exception=True)
        if seriliazer.validated_data.keys():
            queryset = queryset.filter(**seriliazer.validated_data)
        return queryset

    @action(detail=True, methods=['post'])
    def buy(self, request):
        thing_to_buy = self.get_object()
        Transaction.objects.create()


    @action(detail=False, methods=['get'])
    def most(self, request):
        things = self.queryset.annotate(num_tags=Count('tags')).order_by('-num_tags')[:10]
        serializer = self.get_serializer(things, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'])
    def comment(self, request, pk=None):
        thing = self.get_object()
        if request.method == "POST":
            data = {'content': request.data['content'],
                    'user': request.user.id,
                    'object_id': thing.id}
            serializer = CommentSerializer(data=data)

            serializer.is_valid(raise_exception=True)
            Comment.objects.create(**serializer.validated_data, content_object = thing)
            return Response({"Comment": "Created!"})
        else:
            serializer = CommentSerializer(thing.get_comments(), many=True)
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