from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView, CreateView

from answers.forms import AnswerCreateForm
from answers.models import Answer, AnswerView
from languages.models import Language
from questions.models import Question, QuestionStatus
from utils.views import CurrentCountryListViewMixin, MyListViewMixin, ValidationMixin


class CreateAnswerValidationMixin(ValidationMixin):
    def validate(self):
        question_id = self.kwargs.get('question_id')
        country_id = self.kwargs.get('country_id')
        self.question = Question.objects.get(id=question_id, country_id=country_id)

        if self.question.status != QuestionStatus.PUBLISHED:
            messages.error(self.request, _('This question is not published yet'))
            return redirect('answers:index', country_id=country_id, question_id=self.question.id)

        if self.request.user == self.question.author:
            messages.error(self.request, _("Question's author can't answer to it"))
            return redirect('questions:index', country_id=country_id)

        if Answer.objects.filter(author=self.request.user, question=self.question).exists():
            messages.error(self.request, _('You already answered to this question'))
            return redirect('answers:index', country_id=country_id, question_id=self.question.id)


class CreateAnswerView(LoginRequiredMixin, CreateAnswerValidationMixin, CreateView):
    model = Answer
    form_class = AnswerCreateForm
    template_name = 'answers/create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Answer(
            author=self.request.user,
            question=self.question,
            language=Language.get_for_request(self.request),
        )
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.question
        return context


class AnswersListView(CurrentCountryListViewMixin, ListView):
    model = Answer
    queryset = Answer.objects.select_related('question')\
        .annotate(Count('answerview'))
    ordering = 'answerview__count'
    template_name = 'answers/list.html'
    country_field_name = 'question__country_id'


class IndexAnswersListView(AnswersListView):
    def get(self, request, *args, **kwargs):
        question_id = kwargs.get('question_id')
        question = Question.objects.get(id=question_id)
        if question.status in (QuestionStatus.DRAFT, QuestionStatus.DEFERRED):
            return redirect('questions:edit', country_id=kwargs.get('country_id'), pk=question_id)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        queryset = context['object_list']
        if len(queryset) > 0:
            context['question'] = queryset[0].question
        else:
            context['question'] = Question.objects.filter(id=self.kwargs.get('question_id')).get()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(question_id=self.kwargs.get('question_id'))


class MyAnswersListView(MyListViewMixin, AnswersListView):
    pass  # TODO! aggregate by question


class AnswersDetailView(DetailView):
    queryset = Answer.objects.select_related('question')\
        .annotate(Count('answerview'))
    template_name = 'answers/detail.html'

    def get(self, request, *args, **kwargs):
        answer = Answer.objects.filter(pk=self.kwargs.get('pk')).first()
        right_question_statuses = (QuestionStatus.PUBLISHED, QuestionStatus.ANSWERED)
        is_right_question_status = answer and answer.question__status in right_question_statuses
        if request.user.is_authenticated and is_right_question_status:
            AnswerView.objects.get_or_create(answer_id=answer.id, user=request.user)
        return super().get(request, *args, **kwargs)


create = CreateAnswerView.as_view()
index = IndexAnswersListView.as_view()
my = MyAnswersListView.as_view()
detail = AnswersDetailView.as_view()
