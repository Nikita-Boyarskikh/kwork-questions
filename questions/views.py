from annoying.functions import get_object_or_None
from constance import config
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView

from accounts.models import AccountAction, AccountActionType, AccountActionStatus
from countries.models import Country
from languages.models import Language
from questions.forms import QuestionCreateForm
from questions.models import Question, QuestionStatus
from utils.views import CurrentCountryListViewMixin, MyListViewMixin, LoginRequiredMixin, UserAgreementRequiredMixin, \
    AccessWithMessageAdapter


class CreateQuestionView(LoginRequiredMixin, UserAgreementRequiredMixin, CreateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'questions/create.html'
    permission_denied_message = _('Only registered users can create questions.\nPlease, register.')
    accept_agreements_url = reverse_lazy('rules:index')
    agreements_not_accepted_message = _('You should accept site rules to create question.')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        country = Country.get_for_request(self.request) or Country.default
        kwargs['instance'] = Question(
            author=self.request.user,
            price=config.MIN_QUESTION_PRICE,
            language=Language.get_for_request(self.request),
            country=country,
        )
        return kwargs


class UnpublishedQuestionStatusRequiredMixin:
    unpublished_message = _('You can not edit published question')

    def get_redirect_url(self):
        return reverse('answers:index', question_id=self.object.id, country_id=self.kwargs.get('country_id') or 'unknown')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.status not in (QuestionStatus.DRAFT, QuestionStatus.DEFERRED):
            adapter = AccessWithMessageAdapter(self.get_redirect_url(), self.unpublished_message)
            return adapter.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UpdateQuestionView(LoginRequiredMixin, UnpublishedQuestionStatusRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'questions/edit.html'

    def get_success_url(self):
        return reverse('questions:my', kwargs={'country_id': self.kwargs.get('country_id') or 'unknown'})


@transaction.atomic
@login_required
def publish(request, country_id, pk):
    try:
        question = Question.objects.select_for_update().get(pk=pk)
    except Question.DoesNotExist:
        messages.error(request, _('Question with this id does not exist'))
        return redirect('questions:index', country_id=country_id)

    status = QuestionStatus.PENDING
    if status not in question.allowed_status_transitions:
        messages.error(request, _('This question already published'))
        return redirect('questions:index', country_id=country_id)

    if question.author.account.balance < question.price:
        messages.error(request, _('You have no enough money'))
        return redirect('answers:index', question_id=question.id, country_id=country_id)

    AccountAction.objects.create(
        account=question.author.account,
        type=AccountActionType.PAY_SERVICE_FEE,
        delta=-question.price,
        status=AccountActionStatus.APPROVED,
        product=question,
    )
    question.status = status
    question.save()

    messages.success(request, _('Question successfully send to moderation'))

    return redirect(question)


class QuestionsListView(CurrentCountryListViewMixin, ListView):
    model = Question
    template_name = 'questions/list.html'
    allow_empty = True
    url_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = self.url_name
        return context


class QuestionsForStatusListView(QuestionsListView):
    status = None

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status=self.status)


class AnsweredQuestionsListView(QuestionsForStatusListView):
    status = QuestionStatus.ANSWERED
    url_name = 'questions:voting'


class PublishedQuestionsListView(QuestionsForStatusListView):
    status = QuestionStatus.PUBLISHED
    url_name = 'questions:index'


class ClosedQuestionsListView(QuestionsForStatusListView):
    status = QuestionStatus.CLOSED
    url_name = 'questions:closed'


class MyQuestionsListView(MyListViewMixin, QuestionsListView):
    url_name = 'questions:my'


class MyAnsweredQuestionsListView(MyListViewMixin, AnsweredQuestionsListView):
    url_name = 'questions:my_voting'


index = PublishedQuestionsListView.as_view()
create = CreateQuestionView.as_view()
edit = UpdateQuestionView.as_view()
closed = ClosedQuestionsListView.as_view()
answered = AnsweredQuestionsListView.as_view()
my = MyQuestionsListView.as_view()
my_answered = MyAnsweredQuestionsListView.as_view()
