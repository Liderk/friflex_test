from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets

from api.v1.serializers import CourseSerializer, SubscribeSerializer, \
    CourseMaterialsSerializer, CourseScoreSerializer
from courses.models import Course, CourseUsers
from rest_framework.response import Response


class CourseInfoSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """
    api_v1/courses/ [GET] : возвращает информацию о всех курсах,
    если студент подписан на них.

    api_v1/courses/{id}/ [GET] : возвращает курс по указанному id,
    если человек подписан на него
    """
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        student = self.request.user
        queryset = Course.objects.filter(student=student)
        return queryset


class CourseMaterials(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Просмотр всех материалов курса на который подписан студент
    api_v1/courses/materials/{id}/ [GET]
    """
    serializer_class = CourseMaterialsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        student = self.request.user
        queryset = Course.objects.filter(student=student)
        return queryset


class CourseSubscribeSet(viewsets.ModelViewSet):
    """
        api_v1/courses/subscribe/ [GET] - получить все подписи текущего пользователя
        api_v1/courses/subscribe/ [POST] - подписаться на курс
        {
        id: course_id,
        }
        api_v1/courses/subscribe/ [DELETE] - подписаться на курс
    """
    serializer_class = SubscribeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        student = self.request.user
        queryset = CourseUsers.objects.filter(student=student)
        return queryset

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.request.data.get('id'))
        serializer = SubscribeSerializer(data=self.request.data, context={
            'student': self.request.user,
            'course': course
        })
        serializer.is_valid(raise_exception=True)
        serializer.save(student=self.request.user, course=course)

    def destroy(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])
        subscription = get_object_or_404(
            CourseUsers,
            course=course,
            student=request.user)
        subscription.delete()
        return Response({'success': True})


class CourseScoreSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Выставление оценки к курсу."""

    serializer_class = SubscribeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        print(self.kwargs.get('course_id'))
        queryset = get_object_or_404(Course, pk=self.kwargs.get('course_id'))
        return queryset

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs.get('course_id'))
        serializer = CourseScoreSerializer(data=self.request.data, context={
            'student': self.request.user,
            'course': course
        })
        serializer.is_valid(raise_exception=True)
        serializer.save(student=self.request.user, course=course)
