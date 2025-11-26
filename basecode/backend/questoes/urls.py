from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicoViewSet, QuestaoViewSet

router = DefaultRouter()
router.register(r'topicos', TopicoViewSet)
router.register(r'questoes', QuestaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]