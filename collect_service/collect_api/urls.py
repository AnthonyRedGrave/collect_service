from rest_framework import urlpatterns
from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import *

router = SimpleRouter()
router.register('things/list', ThingViewSet)
router.register('thing_messages/list', ThingMessageViewSet)

urlpatterns = [
    path('sections/list/', SectionApiView.as_view(), name='section_list'),
]

urlpatterns += router.urls