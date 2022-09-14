from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView

from answers.forms import AnswerCreateForm
from answers.models import Answer, AnswerView
from languages.models import Language
from questions.models import Question, QuestionStatus
from translate.utils import translate
from utils.views import CurrentCountryListViewMixin, MyListViewMixin


# TODO use generic CreateView
@login_required
def create(request, question_id, country_id):
    question = Question.objects.get(id=question_id, country_id=country_id)
    if question.status != QuestionStatus.PUBLISHED:
        messages.error(request, _('This question is not published yet'))
        return redirect('answers:index', country_id=country_id, question_id=question.id)

    if request.user == question.author:
        messages.error(request, _("Question's author can't answer to it"))
        return redirect('questions:index', country_id=country_id)

    if Answer.objects.filter(author=request.user, question=question).exists():
        messages.error(request, _('You already answered to this question'))
        return redirect('answers:index', country_id=country_id, question_id=question.id)

    answer = Answer(
        author=request.user,
        question=question,
        language=Language.get_for_request(request),
    )
    form = AnswerCreateForm(instance=answer)
    if request.method == 'POST':
        form = AnswerCreateForm(request.POST, instance=answer)
        if form.is_valid():
            # TODO: refactor
            if 'translate' in request.POST:
                new_form_data = form.data.copy()
                new_form_data['en_text'] = translate(
                    text=form.cleaned_data['original_text'],
                    source_language=answer.language,
                    target_language=Language.default,
                )
                form.data = new_form_data
            elif answer.language == Language.default and not form.cleaned_data['en_text']:
                new_form_data = form.data.copy()
                new_form_data['en_text'] = form.cleaned_data['original_text']
                form.data = new_form_data
            elif not form.cleaned_data['en_text']:
                form.add_error('en_text', _('This field is required.'))
            else:
                form.save()
                return redirect(answer)

    response = render(request, 'answers/create.html', {
        'form': form,
    })

    return response


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


index = IndexAnswersListView.as_view()
my = MyAnswersListView.as_view()
detail = AnswersDetailView.as_view()
