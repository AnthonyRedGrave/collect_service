from comments.models import Comment
from comments.serializers import CommentSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import ThingMessage, Thing, Section, Deal
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    CreateDealSerializer,
    SectionSerializer,
    ThingSerializer,
    ThingMessageSerializer,
    DateAndOrderingSerializer,
    UpdateDealSerializer,
    DealModelSerializer
)
from vote.serializers import VoteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import mixins
from django.db.models import Count
from things.services.deal import create_deal
from things.services.csv import csv_export
from vote.services.assesment import create_or_delete_vote
from django.db.models import Q, Sum
import logging
from .filters import ThingFilter

logger = logging.getLogger(__name__)


class ThingMessageViewSet(ReadOnlyModelViewSet):
    queryset = ThingMessage.objects.all()
    serializer_class = ThingMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        logger.info("ThingMessageViewSet GET get_queryset")
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    @action(detail=False, methods=["get"])
    def user_messages(self, request):
        messages = self.queryset.filter(thing__owner = request.user)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data) 


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
    filter_backends = [DjangoFilterBackend]
    filter_class = ThingFilter

    @action(detail=False, methods=['get'])
    def own(self, request):
        things = self.queryset.filter(owner = request.user)
        serializer = self.get_serializer(things, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def rating(self, request):
        logger.info("ThingViewSet GET action rating Получение рейтинга вещей с разницей лайков/дизлайков")
        things = self.queryset.annotate(votes = Sum("vote__value")).order_by("-votes").exclude(votes__isnull=True)
        serializer = self.get_serializer(things, many=True)
        return Response(serializer.data) 


    @action(detail=True, methods=["get", "post"])
    def rate(self, request, pk=None):
        thing = self.get_object()
        request_data = request.GET or request.data
        serializer = VoteSerializer(data = request_data)
        serializer.is_valid(raise_exception=True)
        if request.method == "GET":
            logger.info("ThingViewSet GET action rate Получение всех лайков/дизлайков вещи")
            serializer = VoteSerializer(thing.vote_set.filter(value = serializer.validated_data['value']), many=True)
            return Response(serializer.data)
        else:
            logger.info("ThingViewSet POST action rate Создание нового лайка/дизлайка для вещи")
            response = create_or_delete_vote(thing, request.user, serializer.validated_data['value'])
            serializer = VoteSerializer(response)
            return Response(serializer.data)

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

    @action(detail=True, methods=["get", "post"])
    def message(self, request, pk=None):
        thing = self.get_object()
        if request.method == "POST":
            data = {
                "content": request.data["content"],
                "user": request.user.id,
                "thing": thing.id
            }
            serializer = ThingMessageSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            ThingMessage.objects.create(**serializer.validated_data)
            return Response({"Message": "Created!"})
        else:
            serializer = ThingMessageSerializer(thing.get_messages(), many=True)
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
