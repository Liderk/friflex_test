import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Course(UUIDMixin, TimeStampedMixin, models.Model):
    """Модель существующих курсов."""
    title = models.CharField(verbose_name=_('title'), max_length=150)
    description = models.CharField(_('description'),
                                   max_length=500,
                                   blank=True)
    student = models.ManyToManyField(User, through='CourseUsers')

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')


class PdfFile(UUIDMixin, TimeStampedMixin, models.Model):
    """класс для указания к какому курсу должны привязываться пдф файлы"""

    file_path = models.FileField(_('file'), upload_to='courses/')
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name=_('pdf'))

    class Meta:
        verbose_name = _('pdf')
        verbose_name_plural = _('pdfs')


class TextDescription(UUIDMixin, TimeStampedMixin, models.Model):
    """класс для описании модели текстовой информации к курсу"""

    text = models.TextField(_('text'))
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name=_('text'))

    class Meta:
        verbose_name = _('text')
        verbose_name_plural = _('texts')


class Link(UUIDMixin, TimeStampedMixin, models.Model):
    """класс для описании модели ссылок к курсу"""

    description = models.URLField(_('description'), max_length=200)
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name=_('link'))

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')


class CourseUsers(UUIDMixin, TimeStampedMixin,  models.Model):
    """Модель таблицы описывающая связь пользователей и курсов"""
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('course student')
        verbose_name_plural = _('course student')
