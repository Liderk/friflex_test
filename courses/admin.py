from django.contrib import admin

from courses.models import Course, PdfFile, TextInformation, Link, \
    CourseUsers, CourseScore


class CourseUsersInline(admin.TabularInline):
    model = CourseUsers
    extra = 0


class CoursePdfsInline(admin.TabularInline):
    model = PdfFile
    extra = 0


class CourseLinksInline(admin.TabularInline):
    model = Link
    extra = 0


class CourseTextsInline(admin.TabularInline):
    model = TextInformation
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = (CourseUsersInline,
               CoursePdfsInline,
               CourseLinksInline,
               CourseTextsInline)

    # Отображение полей в списке
    list_display = ('title', 'description', 'avg_score', 'created')


@admin.register(PdfFile)
class PdfFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_path', 'course', 'created')


@admin.register(TextInformation)
class TextDescriptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'course', 'created')


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_text', 'course', 'created')


@admin.register(CourseUsers)
class CourseUsersAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'created')


@admin.register(CourseScore)
class CourseScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'score')
