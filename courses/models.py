from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name=_('created'))

    class Meta:
        abstract = True


class Course(TimeStampedMixin, models.Model):
    """Модель существующих курсов."""
    title = models.CharField(verbose_name=_('title'),
                             max_length=150,
                             blank=False,
                             null=False)
    description = models.CharField(verbose_name=_('description'),
                                   max_length=500,
                                   blank=True)
    student = models.ManyToManyField(User, through='CourseUsers')

    @property
    def avg_score(self):
        scores = self.scores.all().aggregate(Avg('score')).get('score__avg')
        return scores if scores else 0.00

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    def __str__(self):
        return self.title


class PdfFile(TimeStampedMixin, models.Model):
    """класс для указания к какому курсу должны привязываться пдф файлы"""
    file_name = models.CharField(max_length=255,
                                 blank=False,
                                 null=False,
                                 verbose_name=_('file_name'))

    file_path = models.FileField(verbose_name=_('file'),
                                 blank=False,
                                 null=False,
                                 upload_to='course_files/')
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name=_('pdf'),
                               verbose_name=_('course'))

    class Meta:
        verbose_name = _('pdf')
        verbose_name_plural = _('pdfs')

    def __str__(self):
        return self.file_name


class TextInformation(TimeStampedMixin, models.Model):
    """Класс для описания модели текстовой информации к курсу"""
    title = models.CharField(verbose_name=_('title'),
                             max_length=150,
                             blank=False,
                             null=False)
    text = models.TextField(verbose_name=_('text'))
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name='text',
                               verbose_name=_('course'))

    class Meta:
        verbose_name = _('text')
        verbose_name_plural = _('texts')

    def __str__(self):
        return self.title


class Link(TimeStampedMixin, models.Model):
    """Модель описания таблицы ссылок к курсу"""
    title = models.CharField(verbose_name=_('title'),
                             max_length=150,
                             blank=False,
                             null=False)
    link_text = models.URLField(_('link'), max_length=200)
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name='link',
                               verbose_name=_('course'))

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')

    def __str__(self):
        return self.title


class CourseScore(models.Model):
    """Модель таблицы содержащая поставленную оценку курса"""
    student = models.ForeignKey(User,
                                on_delete=models.DO_NOTHING,
                                related_name='rated',
                                verbose_name=_('student'))
    course = models.ForeignKey('Course', on_delete=models.CASCADE,
                               related_name='scores',
                               verbose_name=_('course'))
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name=_('score'))

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
                               related_name='subscription',
                               verbose_name=_('course'))
    student = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='student',
                                verbose_name=_('student'))

    class Meta:
        verbose_name = _('course student')
        verbose_name_plural = _('course student')

    def __str__(self):
        return f'{self.__class__.__name__}(' \
               f'student={self.student},' \
               f'course={self.course},'
