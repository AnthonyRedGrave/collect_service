from rest_framework import urlpatterns
from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import *

router = SimpleRouter()
router.register('things/list', ThingViewSet)
router.register('thing_messages/list', ThingMessageViewSet)
router.register('sections/list', SectionViewSet)

urlpatterns = router.urls