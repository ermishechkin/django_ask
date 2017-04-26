# -*- coding: utf8

from __future__ import unicode_literals
import datetime
import os

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import F, Count
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name = u"Пользователь Django", primary_key=True)
    name = models.CharField(max_length=255, verbose_name = u"Имя")
    avatar = models.ImageField(upload_to='uploads',
                               verbose_name = u"Файл аватарки")

    class Meta:
        verbose_name = u"Профиль"
        verbose_name_plural = u"Профили"

    def __unicode__(self):
        return self.name

    def avatar_url(self):
        return '/' + str(self.avatar)


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name = u"Заголовок вопроса", primary_key=True)

    class Meta:
        verbose_name = u"Тэг"
        verbose_name_plural = u"Тэги"

    def __unicode__(self):
        return self.name


class QuestionManager(models.Manager):
    def get_newest(self):
        # return super(QuestionManager, self).get_queryset()
        return super(QuestionManager, self).get_queryset().order_by('-published')

    def get_hottest(self):
        return super(QuestionManager, self).get_queryset().all().annotate(
                     interest = Count('marks')).order_by('-interest')

    def get_by_id(self, id):
        return super(QuestionManager, self).get_queryset().get(id = id)

    def get_queryset(self):
        return super(QuestionManager, self).get_queryset()

    def get_by_tag(self, tag):
        return super(QuestionManager, self).get_queryset().filter(tags=tag).order_by('-published')

class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name = u"Заголовок вопроса")
    text = models.TextField(verbose_name = u"Текст")
    author = models.ForeignKey(Profile, verbose_name = u"Автор",
                               related_name='%(class)sauthor', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank = True, verbose_name = u"Тэги")
    marks = models.ManyToManyField(Profile, blank = True,
                                   through = 'MarkQuestion',
                                   through_fields=('question', 'author'),
                                   verbose_name = u"Оценки",
                                   related_name='%(class)smarked_by')
    published = models.DateTimeField(verbose_name = u"Дата и время создания")
    objects = QuestionManager()

    class Meta:
        verbose_name = u"Вопрос"
        verbose_name_plural = u"Вопросы"

    def __unicode__(self):
        return self.title

    def raiting(self):
        ms = MarkQuestion.objects.filter(question=self).all()
        return sum(1 if m.is_good else -1 for m in ms)

    def answers(self):
        return Answer.objects.filter(question = self)

    def get_url(self):
        return reverse('question', kwargs={'id' : self.id })

class Answer(models.Model):
    text = models.TextField(verbose_name = u"Текст")
    author = models.ForeignKey(Profile, verbose_name = u"Автор",
                               related_name='%(class)sauthor')
    marks = models.ManyToManyField(Profile, blank = True,
                                   through = 'MarkAnswer',
                                   through_fields=('answer', 'author'),
                                   verbose_name = u"Оценки",
                                   related_name='%(class)smarked_by')
    question = models.ForeignKey(Question, verbose_name = u"Вопрос", on_delete=models.CASCADE)

    class Meta:
        verbose_name = u"Ответ"
        verbose_name_plural = u"Ответы"

    def __unicode__(self):
        return self.text

    def raiting(self):
        ms = MarkAnswer.objects.filter(answer=self).all()
        return sum(1 if m.is_good else -1 for m in ms)

class MarkAnswer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_good = models.BooleanField(verbose_name = u"Лайк/Дизлайк")
    class Meta:
        verbose_name = u"Оценка ответа"
        verbose_name_plural = u"Оценки ответа"
    def __unicode__(self):
        return u"Лайк" if self.is_good == True else u"Дизлайк"

class MarkQuestion(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_good = models.BooleanField(verbose_name = u"Лайк/Дизлайк")
    class Meta:
        verbose_name = u"Оценка вопроса"
        verbose_name_plural = u"Оценки вопроса"
    def __unicode__(self):
        return u"Лайк" if self.is_good == True else u"Дизлайк"
