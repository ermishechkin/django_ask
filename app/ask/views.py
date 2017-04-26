# -*- coding: utf8

from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from ask.forms import QuestionForm, SignupForm, AnswerForm
from ask.paginator import paginate, PaginatorError
from ask.models import Profile, Answer, Question, Tag, Profile, MarkQuestion, MarkAnswer
from datetime import datetime
from json import loads

def ajax_login_required(view):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse(data={ 'status' : 'error', 'msg' : 'not auth' })
        return view(request, *args, **kwargs)
    return wrapper

def test(request) :
    result = "<h2> GET variables </h2>"
    for v in request.GET.items() :
        result += v[0] + '  =  ' + v[1] + '<br>'

    result += "<h2> POST variables </h2>"
    for v in request.POST.items() :
        result += v[0] + '  =  ' + v[1] + '<br>'

    return HttpResponse(result)

def list_questions(request, questions, page, title, base_url):
    try:
        q, paginator = paginate(questions, page)
    except PaginatorError:
        raise Http404()
    if request.user.is_authenticated():
        for m in MarkQuestion.objects.filter(author = request.profile,
                                             question__in = q):
            for question in q:
                if m.question == question:
                    if m.is_good:
                        question.liked = True
                    else:
                        question.disliked = True
    return render(request, 'questions.html', { 'title' : title,
                                               'questions' : q,
                                               'paginator' : paginator,
                                               'base_url' : base_url })


def index(request, page='1') :
    newest = Question.objects.get_newest()
    title = 'Новые вопросы'
    base_url = reverse('index')
    return list_questions(request, newest, page, title, base_url)

def hot(request, page='1') :
    hottest = Question.objects.get_hottest()
    title = 'Интереснейшие вопросы'
    base_url = reverse('hot')
    return list_questions(request, hottest, page, title, base_url)

def tag(request, name, page=1) :
    tag = Tag.objects.filter(name=name)
    if tag.exists():
        by_tag = Question.objects.get_by_tag(tag.first())
    else:
        raise Http404
    title = u'Поиск по тэгу \'' + name + '\''
    base_url = reverse('tag', kwargs={ 'name': name })
    return list_questions(request, by_tag, page, title, base_url)

@login_required(redirect_field_name='continue')
# @login_required()
def ask(request) :
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            q = Question(title = data['title'], text = data['content'],
                         author = request.profile, published = datetime.now())
            q.save()
            q.tags.add(*[Tag.objects.get_or_create(name=t)[0] for t in data['tags']])
            return redirect(reverse('question', kwargs={ 'id': q.id }))
    else:
        form = QuestionForm()
    return render(request, 'ask.html', { 'form' : form })

def signup(request) :
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(data['nick'],
                                            data['email'], data['password'])
            p = Profile(user=user, name=data['name'],
                        avatar=request.FILES['avatar'])
            p.save()
            user = authenticate(username=data['nick'],
                                password=data['password'])
            login(request, user)
            return redirect(reverse('index'))
    else:
        form = SignupForm()
    return render(request, 'signup.html', { 'form' : form })

def question(request, id, page=1) :
    try:
        q = Question.objects.get(id=id)
    except int:
        return Http404()

    try:
        a, paginator = paginate(Answer.objects.filter(question_id = q.id).all(), page)
    except PaginatorError:
        raise Http404()

    is_author = False
    if request.user.is_authenticated():
        is_author = (q.author == request.profile)
        m = MarkQuestion.objects.filter(question=q, author=request.profile)
        if m.exists():
            q.liked = (m[0].is_good == True)
            q.disliked = (m[0].is_good == False)
        for m in MarkAnswer.objects.filter(author = request.profile, answer__in = a):
            for answer in a:
                if m.answer == answer:
                    if m.is_good:
                        answer.liked = True
                    else:
                        answer.disliked = True
    base_url = reverse('question', kwargs={ 'id': id })
    return render(request, 'question.html', { 'question' : q,
                                              'answers' : a,
                                              'base_url' : base_url,
                                              'paginator' : paginator,
                                              'is_author' : is_author,
                                            })

from requests import post
@require_POST
@ajax_login_required
def add_answer(request):
    try:
        data = request.POST
        qid = int(data['qid'])
        content = data['content']
        a = Answer(text=content, author=request.profile, question_id=qid)
        a.save()

        ans_html = str(render_to_response('a.html', { 'answer' : a }).content)
        post('https://alex-erm.ru/pub?id='+str(qid), ans_html)

        return JsonResponse(data={ 'status' : 'OK', 'id' : a.id })
    except Exception:
        return JsonResponse(data={ 'status' : 'error', 'msg' : 'incorrect request' })

def login2(request) :
    was_failed = False
    if request.method == 'POST' :
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            target = request.GET.get('continue', reverse('index'))
            return redirect(target)
        was_failed = True
    return render(request, 'login.html', { 'failed' : was_failed })

def logout2(request):
    logout(request)
    target = request.META.get('HTTP_REFERER', reverse('index'))
    return redirect(to=target)


@require_POST
@ajax_login_required
def setMarkQuestion(request):
    data = request.POST
    qid = int(data['qid'])
    q = Question.objects.get(id = qid)
    val = data['mark']
    if val=='like':
        val = 1
    elif val=='dislike':
        val = -1
    else:
        val = None # error
    m = MarkQuestion.objects.filter(question_id=qid, author=request.profile)
    if m.exists():
        m = m.first()
        m.is_good = (val==1)
    else:
        m = MarkQuestion(question_id=qid, author=request.profile, is_good=(val==1))
    m.save()
    return JsonResponse( {'status' : 'ok', 'qid' : qid, 'mark': val, 'total' : q.raiting() } )

@require_POST
@ajax_login_required
def setMarkAnswer(request):
    data = request.POST
    aid = int(data['aid'])
    a = Answer.objects.get(id = aid)
    val = data['mark']
    if val=='like':
        val = 1
    elif val=='dislike':
        val = -1
    else:
        val = None # error
    m = MarkAnswer.objects.filter(answer_id=aid, author=request.profile)
    if m.exists():
        m = m.first()
        m.is_good = (val==1)
    else:
        m = MarkAnswer(answer_id=aid, author=request.profile, is_good=(val==1))
    m.save()
    return JsonResponse( {'status' : 'ok', 'aid' : aid, 'mark': val, 'total' : a.raiting() } )
