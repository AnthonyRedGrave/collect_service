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
from datetime import datetime


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
    def buy_accept(self, request, pk=None):
        thing_to_buy = self.get_object()
        status_log = {"accept":
                        {"status": "Принят",
                         "date": str(datetime.now()),
                         "owner": thing_to_buy.owner.username,
                         "customer": request.user.username}
                    }
        transaction = Transaction.objects.create(owner = thing_to_buy.owner, customer = request.user, status = "Accepted", thing = thing_to_buy, status_log= status_log)
        transaction.save()
        return Response(status_log)


    @action(detail=True, methods=['post'])
    def buy_confirm(self, request, pk=None):
        thing_to_buy = self.get_object()
        transaction = Transaction.objects.get(thing = thing_to_buy, owner = thing_to_buy.owner, customer = request.user)
        status_log = {"confirm":
                        {"status": "Подтвержден",
                         "date": str(datetime.now()),
                         "owner": transaction.owner.username,
                         "customer": transaction.customer.username,
                         "cost": str(thing_to_buy.price)}
                    }
        transaction.status_log.update(status_log)
        transaction.status = "Confirmed"
        transaction.cost = thing_to_buy.price
        transaction.save()
        return Response(status_log)

    #поговорить о том, нужны ли все таки транзакции
    @action(detail=True, methods=['post'])
    def buy_complete(self, request, pk=None):
        thing_to_buy = self.get_object()
        transaction = Transaction.objects.get(thing = thing_to_buy, owner = thing_to_buy.owner, customer = request.user)
        status_log = {"complete":
                        {"status": "Выполнен",
                         "date": str(datetime.now()),
                         "new_owner": transaction.customer.username,
                         "old_owner": transaction.owner.username,
                         "cost": str(thing_to_buy.price)}
                    }
        thing_to_buy.owner = request.user
        thing_to_buy.save()
        transaction.status = "Completed"
        transaction.status_log.update(status_log)
        transaction.save()
        return Response(status_log)


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