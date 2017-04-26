from django.contrib import admin
from ask.models import Profile
from ask.models import Question
from ask.models import Answer
from ask.models import Tag
from ask.models import MarkAnswer
from ask.models import MarkQuestion


class ProfileAdmin(admin.ModelAdmin):
    pass

class QuestionAdmin(admin.ModelAdmin):
    pass

class AnswerAdmin(admin.ModelAdmin):
    pass

class TagAdmin(admin.ModelAdmin):
    pass

class MarkAnswerAdmin(admin.ModelAdmin):
    pass

class MarkQuestionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(MarkAnswer, MarkAnswerAdmin)
admin.site.register(MarkQuestion, MarkQuestionAdmin)
