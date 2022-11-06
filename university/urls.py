# urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import RelatedViewSet
from . import views


router = DefaultRouter()
router.register(r'relations', RelatedViewSet, basename="relations")

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.index, name='index')
]