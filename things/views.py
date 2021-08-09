from comments.models import Comment
from comments.serializers import CommentSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import ThingMessage, Thing, Section, Deal
from .serializers import (
    CreateDealSerializer,
    SectionSerializer,
    ThingSerializer,
    ThingMessageSerializer,
    DateSerializer,
    UpdateDealSerializer,
    DealModelSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import mixins
from django.db.models import Count
from things.services.deal import create_deal
from things.services.csv import csv_export


class ThingMessageViewSet(ReadOnlyModelViewSet):
    queryset = ThingMessage.objects.all()
    serializer_class = ThingMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def create(self):
        pass

    def destroy(self):
        pass

    def update(self):
        pass


class ThingViewSet(mixins.CreateModelMixin, ReadOnlyModelViewSet):
    queryset = (
        Thing.objects.all()
        .prefetch_related("tags", "comments")
        .select_related("owner", "section")
    )
    serializer_class = ThingSerializer
    permission_classes = [IsAuthenticated]
    # http_method_names = ['get', 'post', 'head']
    # things = Thing.objects.all().prefetch_related('tags').annotate(num_tags=Count('tags'))

    def get_queryset(self):
        queryset = super().get_queryset()
        seriliazer = DateSerializer(data=self.request.query_params)
        seriliazer.is_valid(raise_exception=True)
        if seriliazer.validated_data.keys():
            queryset = queryset.filter(**seriliazer.validated_data)
        return queryset

    @action(detail=False, methods=["get"])
    def csv_export(self, request):
        filename = self.request.query_params.get("filename", "export.csv")
        csv_export(filename)
        return Response("Успешно экспортировано")

    @action(detail=False, methods=["get"])
    def most(self, request):
        things = self.queryset.annotate(num_tags=Count("tags")).order_by("-num_tags")[
            :10
        ]
        serializer = self.get_serializer(things, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get", "post"])
    def comment(self, request, pk=None):
        thing = self.get_object()
        if request.method == "POST":
            data = {
                "content": request.data["content"],
                "user": request.user.id,
                "object_id": thing.id,
            }
            serializer = CommentSerializer(data=data)

            serializer.is_valid(raise_exception=True)
            Comment.objects.create(**serializer.validated_data, content_object=thing)
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


class DealViewSet(
    mixins.UpdateModelMixin, mixins.CreateModelMixin, ReadOnlyModelViewSet
):
    queryset = Deal.objects.all()
    serializer_class = DealModelSerializer

    def get_queryset(self):
        return super().get_queryset().filter(thing__owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateDealSerializer
        elif self.action == "partial_update":
            return UpdateDealSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        create_deal(self.request.user, **serializer.validated_data)
