from rest_framework.routers import SimpleRouter
from django.urls import path


from .views import ThingMessageViewSet, ThingViewSet, SectionViewSet, DealViewSet
from comments.views import CommentViewSet

router = SimpleRouter()
router.register('things', ThingViewSet)
router.register('thing_messages', ThingMessageViewSet)
router.register('sections', SectionViewSet)
router.register('comments', CommentViewSet)
router.register('deals', DealViewSet)

urlpatterns = router.urls