from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from .views import CourseInfoSet, CourseSubscribeSet, CourseMaterials, \
    CourseScoreSet

router = DefaultRouter()

router.register(r'courses/materials', CourseMaterials, basename='materials')

router.register(r'courses/subscribe', CourseSubscribeSet, basename='subscribe')

router.register(r'courses', CourseInfoSet, basename='courses')
router.register(r'courses/(?P<course_id>\d+)/score',
                CourseScoreSet,
                basename='score')

urlpatterns = [
    path('', include(router.urls)),
]