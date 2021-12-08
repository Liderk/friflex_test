from django.contrib import admin

from courses.models import Course, PdfFile, TextDescription, Link, User


class PersonFilmworkInline(admin.TabularInline):
    model = User


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # inlines = (PdfFile, TextDescription, Link, student)

    # Отображение полей в списке
    list_display = ('title', 'description', 'student', 'created',)


@admin.register(PdfFile)
class PdfFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'student', 'created',)
