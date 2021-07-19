from rest_framework.routers import SimpleRouter
from .views import ThingMessageViewSet, ThingViewSet, SectionViewSet
from comments.views import CommentViewSet

router = SimpleRouter()
router.register("things", ThingViewSet)
router.register("thing_messages", ThingMessageViewSet)
router.register("sections", SectionViewSet)
router.register("comments", CommentViewSet)

urlpatterns = router.urls
