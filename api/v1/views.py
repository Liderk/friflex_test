from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets

from api.v1.serializers import CourseSerializer
from courses.models import Course


class CourseInfoSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """
    api_v1/courses/ [GET] : возвращает все курсы, если человек подписан на них
    api_v1/courses/{id}/ [GET] : возвращает курс по указанному id, если человек подписан на него
    """
    serializer_class = CourseSerializer

    def get_queryset(self):
        student = self.request.user
        queryset = Course.objects.all().filter(student=student)
        return queryset
