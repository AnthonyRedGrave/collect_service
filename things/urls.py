from rest_framework import urlpatterns
from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import *

router = SimpleRouter()
router.register('things', ThingViewSet)
router.register('thing_messages', ThingMessageViewSet)
router.register('sections', SectionViewSet)

urlpatterns = router.urls