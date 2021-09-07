from rest_framework.routers import SimpleRouter


from .views import ThingMessageViewSet, ThingViewSet, SectionViewSet, DealViewSet
from comments.views import CommentViewSet
from tags.views import TagViewSet

router = SimpleRouter()
router.register('things', ThingViewSet)
router.register('thing_messages', ThingMessageViewSet)
router.register('sections', SectionViewSet)
router.register('comments', CommentViewSet)
router.register('deals', DealViewSet)
router.register('tags', TagViewSet)

urlpatterns = router.urls