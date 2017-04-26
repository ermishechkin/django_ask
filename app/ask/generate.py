from random import randrange, sample, randint
from datetime import datetime as dt, timedelta
from ask.models import *

def gen_many():
    # tags
    tags = ['perl', 'python', 'TechnoPark', 'MySQL', 'django',
            'Mail.Ru', 'Voloshin', 'Firefox','science', 'computer',
            'HTML', 'CSS', 'bootstrap']
    for t in tags:
        Tag(name = t).save()

    def random_date(start, end):
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)

    #authors
    for first_name in ['Вася', 'Петя', 'Алексей', 'Саша', 'Сергей',
                       'Никита', 'Егор', 'Олег', 'Илья', 'Дима']:
        for second_name in ['Григорьев', 'Попов', 'Иванов', 'Сидоров', 'Семенов',
                            'Петров', 'Воробьев', 'Соловьев', 'Макаров', 'Синицин']:
            d1 = dt.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
            d2 = dt.strptime('1/1/2009 4:50 AM', '%m/%d/%Y %I:%M %p')
            u = User.objects.create_user(first_name + second_name, first_name + second_name + '@test.com', '1234')
            u.save()
            birthday = random_date(d1, d2)
            Profile(user=u, name = first_name + ' ' + second_name).save()

    #return
    # questions
    ti = ['Some title', 'What is ...?', 'How many ...?', 'How long ...?', 'Why ...?']
    te = ['some text '*10, 'very big question content '*70, 'middle size '*30,]
    au_c = Profile.objects.all().count()
    t_c = min(6, Tag.objects.all().count())
    p_c = Profile.objects.all().count()

    for i in range(0, 400):
        title = ti[randint(0, len(ti)-1)] + ' (' + str(i) + ')'
        text = te[randint(0, len(te)-1)] + ' (' + str(i) + ')'
        author_id = randint(0, au_c-1) + 1
        tag = sample(range(0, t_c), randint(0, t_c-1))
        tag = [tags[i] for i in tag]
        marks = sample(range(1, p_c + 1), randint(0, t_c-1))
        d1 = dt.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
        d2 = dt.strptime('1/1/2009 4:50 AM', '%m/%d/%Y %I:%M %p')
        published = random_date(d1, d2)
        q = Question(title = title, text = text, author_id = author_id, published = published)
        q.save()
        q.tags.add(*tag)
        q.save()

        for i in range(0, randint(0, 7)):
            Answer(text = 'text ' + str(i), author_id = randint(0, au_c-1) + 1, question = q).save()

    #a = Profile.objects.all()[0]
    #q = Question(title = 'Some title', text = 'some text'*30, author=a,
    #             published = datetime.datetime.now())
    #q.save()


















# class MarkAnswer(models.Model):
#     is_good = models.BooleanField(verbose_name = u"Лайк/Дизлайк")
#
#     class Meta:
#         verbose_name = u"Оценка ответа"
#         verbose_name_plural = u"Оценки ответа"
#
#     def __unicode__(self):
#         return u"Лайк" if self.is_good == True else u"Дизлайк"

# class MarkQuestion(models.Model):
#     is_good = models.BooleanField(verbose_name = u"Лайк/Дизлайк")
#
#     class Meta:
#         verbose_name = u"Оценка вопроса"
#         verbose_name_plural = u"Оценки вопроса"
#
#     def __unicode__(self):
#         return u"Лайк" if self.is_good == True else u"Дизлайк"
