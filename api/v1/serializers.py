from django.contrib.auth import get_user_model
from rest_framework import serializers

from courses.models import PdfFile, TextInformation, Link, Course, CourseUsers, \
    CourseScore

User = get_user_model()


class PdfFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PdfFile
        fields = '__all__'


class TextInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextInformation
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'description', 'avg_score')
        model = Course


class CourseMaterialsSerializer(serializers.ModelSerializer):
    pdf = PdfFilesSerializer(many=True, read_only=True)
    link = LinkSerializer(many=True, read_only=True)
    text = TextInformationSerializer(many=True, read_only=True)

    class Meta:
        fields = ('title', 'pdf', 'link', 'text')
        model = Course


class SubscribeSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(read_only=True)
    student = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = CourseUsers

    def validate(self, data):
        super().validate(data)
        student = self.context.get('student')
        course = self.context.get('course')
        if CourseUsers.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError('subscriptions already created')
        return data


class CourseScoreSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(read_only=True)
    student = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = CourseScore

    def validate(self, data):
        super().validate(data)
        student = self.context.get('student')
        course = self.context.get('course')
        if CourseScore.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError('the assessment has already'
                                              ' been made')
        return data
