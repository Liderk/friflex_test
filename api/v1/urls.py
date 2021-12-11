from django.urls import include, path
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
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
