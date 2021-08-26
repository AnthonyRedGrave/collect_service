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
    AssesmentSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import mixins
from django.db.models import Count
from things.services.deal import create_deal
from things.services.csv import csv_export
from things.services.assesment import create_assesment
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


class ThingMessageViewSet(ReadOnlyModelViewSet):
    queryset = ThingMessage.objects.all()
    serializer_class = ThingMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        logger.info("ThingMessageViewSet GET get_queryset")
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

    def get_queryset(self):
        logger.info("ThingViewSet GET get_queryset")
        queryset = super().get_queryset()
        seriliazer = DateSerializer(data=self.request.query_params)
        seriliazer.is_valid(raise_exception=True)
        if seriliazer.validated_data.keys():
            queryset = queryset.filter(**seriliazer.validated_data)
        return queryset

    @action(detail=True, methods=["get", "post"], name='like')
    def assess(self, request, pk=None):
        thing = self.get_object()
        assesment_type = request.data['type']
        if request.method == "GET":
            logger.info("ThingViewSet GET action asses Получение всех лайков/дизлайков вещи")
            serializer = AssesmentSerializer(thing.get_assessments(assesment_type), many=True)
            return Response(serializer.data)
        else:
            logger.info("ThingViewSet POST action asses Создание нового лайка/дизлайка для вещи")
            request_data = {
                "thing": thing.id,
                "owner": request.user.id,
                "type": assesment_type
            }
            serializer = AssesmentSerializer(data = request_data)
            serializer.is_valid(raise_exception=True)
            responce = create_assesment(serializer.validated_data)
            return Response(responce)

    @action(detail=False, methods=["get"])
    def csv_export(self, request):
        filename = self.request.query_params.get("filename", "export.csv")
        logger.info("ThingViewSet POST action csv_exrport Экспорт записей в csv файл", {'filename': filename})
        csv_export(filename)
        return Response("Успешно экспортировано")

    @action(detail=False, methods=["get"])
    def most(self, request):
        logger.info("ThingViewSet POST action most Получение вещей с наибольшим кол-вом тегов")
        things = self.queryset.annotate(num_tags=Count("tags")).order_by("-num_tags")[
            :10
        ]
        serializer = self.get_serializer(things, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get", "post"])
    def comment(self, request, pk=None):
        thing = self.get_object()
        if request.method == "POST":
            logger.info("ThingViewSet POST action comment")
            data = {
                "content": request.data["content"],
                "user": request.user.id,
                "object_id": thing.id,
            }
            serializer = CommentSerializer(data=data)

            serializer.is_valid(raise_exception=True)
            logger.info("ThingViewSet POST action comment Создание комментария для вещи")
            Comment.objects.create(**serializer.validated_data, content_object=thing)
            return Response({"Comment": "Created!"})
        else:
            logger.info("ThingViewSet GET action comment Получение всех комментариев вещи")
            serializer = CommentSerializer(thing.get_comments(), many=True)
            return Response(serializer.data)

    def perform_create(self, serializer):
        logger.info("ThingViewSet perform create Создание вещи")
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
        logger.info("DealViewSet GET get_queryset")
        return super().get_queryset().filter(Q(old_owner=self.request.user) | Q(new_owner=self.request.user))

    def get_serializer_class(self):
        logger.info("DealViewSet get_serializer_class")
        if self.action == "create":
            return CreateDealSerializer
        elif self.action == "partial_update":
            return UpdateDealSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        logger.info("DealViewSet perform create")
        create_deal(self.request.user, **serializer.validated_data)
