# -*- coding: utf8

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from ask.models import Profile

class SignupForm(forms.Form):
    nick = forms.CharField(max_length=10)
    email = forms.EmailField(max_length=100)
    name = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    avatar = forms.FileField()

    def clean_nick(self):
        nick = self.cleaned_data['nick']
        if ' ' in nick:
            raise forms.ValidationError(u'Ник не должен содержать пробелы')
        if User.objects.filter(username=nick).exists():
            raise forms.ValidationError(u'Ник уже существует')
        return nick

class QuestionForm(forms.Form):
    title = forms.CharField(max_length=255)
    content = forms.CharField()
    tags = forms.CharField(required=False)

    def clean_tags(self):
        def check_tag(tag):
            if len(tag) == 0:
                return False
            return True
        res = self.cleaned_data['tags'].split(',')
        res = [r.strip() for r in res if check_tag(r.strip())]
        return res

class AnswerForm(forms.Form):
    content = forms.CharField()
