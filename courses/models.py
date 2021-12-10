import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Course(TimeStampedMixin, models.Model):
    """Модель существующих курсов."""
    title = models.CharField(verbose_name=_('title'),
                             max_length=150,
                             blank=False,
                             null=False)
    description = models.CharField(_('description'),
                                   max_length=500,
                                   blank=True)
    student = models.ManyToManyField(User, through='CourseUsers')

    avg_score = models.FloatField(blank=False,
                                  null=False,
                                  default=0)

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    def __str__(self):
        return f'{self.__class__.__name__}(' \
               f'title={self.title},' \
               f'description={self.description})'


class PdfFile(TimeStampedMixin, models.Model):
    """класс для указания к какому курсу должны привязываться пдф файлы"""
    file_name = models.CharField(max_length=255,
                                 blank=False,
                                 null=False,
                                 verbose_name=_('file_name'))

    file_path = models.FileField(_('file'),
                                 blank=False,
                                 null=False,
                                 upload_to='course_files/')
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name=_('pdf'))

    class Meta:
        verbose_name = _('pdf')
        verbose_name_plural = _('pdfs')

    def __str__(self):
        return f'{self.__class__.__name__}(' \
               f'file_name={self.file_name},' \
               f'file_path={self.file_path})'


class TextInformation(TimeStampedMixin, models.Model):
    """класс для описании модели текстовой информации к курсу"""
    title = models.CharField(verbose_name=_('title'),
                             max_length=150,
                             blank=False,
                             null=False)
    text = models.TextField(_('text'))
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name=_('text'))

    class Meta:
        verbose_name = _('text')
        verbose_name_plural = _('texts')

    def __str__(self):
        return f'{self.__class__.__name__}(' \
               f'title={self.title},' \
               f'text={self.text[20:]})'


class Link(TimeStampedMixin, models.Model):
    """Модель описания таблицы ссылок к курсу"""
    title = models.CharField(verbose_name=_('title'),
                             max_length=150,
                             blank=False,
                             null=False)
    link_text = models.URLField(_('link'), max_length=200)
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name=_('link'))

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')

    def __str__(self):
        return f'{self.__class__.__name__}(' \
               f'title={self.title},' \
               f'link_text={self.link_text})'


class CourseScore(models.Model):
    """Модель таблицы содержащая поставленную оценку курса"""
    student = models.ForeignKey(User,
                                on_delete=models.DO_NOTHING,
                                related_name=_('rated'),
                                verbose_name=_('student'))
    course = models.ForeignKey('Course', on_delete=models.CASCADE,
                               related_name='scores',
                               verbose_name=_('course'))
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка')

    class Meta:
        verbose_name = _('score')
        verbose_name_plural = _('scores')

    def __str__(self):
        return f'{self.__class__.__name__}(' \
               f'student={self.student},' \
               f'course={self.course},' \
               f'score={self.score})'


class CourseUsers(TimeStampedMixin, models.Model):
    """Модель таблицы содержащих подписанных на курс студентов"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='subscription')
    student = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='student')

    class Meta:
        verbose_name = _('course student')
        verbose_name_plural = _('course student')
