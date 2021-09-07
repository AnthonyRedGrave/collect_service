from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Tag
from .serializers import TagSerializer
from rest_framework.permissions import IsAuthenticated


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def create(self):
        pass

    def destroy(self):
        pass

    def update(self):
        pass