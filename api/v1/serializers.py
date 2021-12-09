from django.contrib.auth import get_user_model
from rest_framework import serializers

from courses.models import PdfFile, TextInformation, Link, Course

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
    pdf = PdfFilesSerializer(many=True, read_only=True)
    link = LinkSerializer(many=True, read_only=True)
    text = TextInformationSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        model = Course
