from django.contrib import admin
from django.contrib.admin import TabularInline

from accounts.admin import AccountActionGenericInline
from answers.admin import AnswerInline
from likes.admin import LikeInline
from questions.models import Question, Comment
from utils.admin import AddingDeniedMixin, DeletingDeniedMixin


# TODO: make it deletable and addable for admin
class BaseQuestionAdmin(AddingDeniedMixin, DeletingDeniedMixin):
    # TODO: make it editable for admin
    readonly_fields = ('en_title', 'original_title', 'en_text', 'original_text', 'price', 'country', 'language')


class QuestionInline(BaseQuestionAdmin, TabularInline):
    model = Question
    extra = 0


class QuestionAdmin(BaseQuestionAdmin, admin.ModelAdmin):
    inlines = (AnswerInline, LikeInline, AccountActionGenericInline)
    list_filter = (
        'author',
        'best_answer',
        'status',
        'country',
        'language',
    )
    list_display = ('__str__', 'status', 'price', 'en_title', 'truncated_en_text', 'author', 'best_answer', 'country')
    search_fields = ('en_text', 'original_text', 'author')
    list_editable = ('status',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Comment)
