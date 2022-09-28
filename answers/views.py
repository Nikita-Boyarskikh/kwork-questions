from annoying.functions import get_object_or_None
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView, CreateView

from answers.forms import AnswerCreateForm
from answers.models import Answer, AnswerView
from languages.models import Language
from questions.models import Question, QuestionStatus
from utils.views import CurrentCountryListViewMixin, MyListViewMixin, LoginRequiredMixin, AccessWithMessageAdapter


class CreateAnswerValidationMixin:
    unpublished_question_message = _('This question is not published yet')
    answer_on_self_question_message = _("Question's author can't answer to it")
    already_answered_message = _('You already answered to this question')

    def get_unpublished_question_url(self):
        return reverse('answers:index', kwargs={
            'question_id': self.question.id,
            'country_id': self.kwargs.get('country_id'),
        })

    def get_answer_on_self_question_url(self):
        return reverse('questions:index', kwargs={'country_id': self.kwargs.get('country_id')})

    def get_already_answered_url(self):
        return reverse('answers:index', kwargs={
            'country_id': self.kwargs.get('country_id'),
            'question_id': self.question.id,
        })

    def dispatch(self, request, *args, **kwargs):
        self.question = Question.objects.get(id=kwargs.get('question_id'), country_id=kwargs.get('country_id'))

        if self.question.status != QuestionStatus.PUBLISHED:
            adapter = AccessWithMessageAdapter(self.get_unpublished_question_url(), self.unpublished_question_message)
            return adapter.permission_denied_response(request)

        if request.user == self.question.author:
            adapter = AccessWithMessageAdapter(self.get_answer_on_self_question_url(), self.answer_on_self_question_message)
            return adapter.permission_denied_response(request)

        if Answer.objects.filter(author=request.user, question=self.question).exists():
            adapter = AccessWithMessageAdapter(self.get_already_answered_url(), self.already_answered_message)
            return adapter.permission_denied_response(request)

        return super().dispatch(request, *args, **kwargs)


class CreateAnswerView(LoginRequiredMixin, CreateAnswerValidationMixin, CreateView):
    model = Answer
    form_class = AnswerCreateForm
    template_name = 'answers/create.html'
    permission_denied_message = _('Only registered users can answer questions.\nPlease, register')

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
        answer = get_object_or_None(Answer.objects.filter(pk=self.kwargs.get('pk')))
        right_question_statuses = (QuestionStatus.PUBLISHED, QuestionStatus.ANSWERED)
        is_right_question_status = answer and answer.question__status in right_question_statuses
        if request.user.is_authenticated and is_right_question_status:
            AnswerView.objects.get_or_create(answer_id=answer.id, user=request.user)
        return super().get(request, *args, **kwargs)


create = CreateAnswerView.as_view()
index = IndexAnswersListView.as_view()
my = MyAnswersListView.as_view()
detail = AnswersDetailView.as_view()
