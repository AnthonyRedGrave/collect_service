from rest_framework.routers import SimpleRouter


from .views import *

router = SimpleRouter()
router.register('things', ThingViewSet)
router.register('thing_messages', ThingMessageViewSet)
router.register('sections', SectionViewSet)

urlpatterns = router.urls