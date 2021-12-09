from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from .views import CourseInfoSet

router = DefaultRouter()

router.register(r'courses', CourseInfoSet, basename='courses')

urlpatterns = [
    path('', include(router.urls)),
]