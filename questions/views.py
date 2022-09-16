from constance import config
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView

from accounts.models import AccountAction, AccountActionType, AccountActionStatus
from languages.models import Language
from questions.forms import QuestionCreateForm
from questions.models import Question, QuestionStatus
from utils.views import CurrentCountryListViewMixin, MyListViewMixin, ValidationMixin


class CreateQuestionValidationMixin(ValidationMixin):
    def validate(self):
        if not self.request.user.is_authenticated:
            messages.info(self.request, _('Only registered users can create questions.\nPlease, register.'))
            return redirect_to_login(self.request.get_full_path_info())

        if not self.request.user.is_user_agreement_accepted:
            messages.info(self.request, _('You should accept site rules to create question.'))
            return redirect('rules:index')


class CreateQuestionView(CreateQuestionValidationMixin, CreateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'questions/create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        country_id = self.kwargs.get('country_id')
        if country_id == 'None':
            country_id = self.request.user.country_id
        kwargs['instance'] = Question(
            author=self.request.user,
            price=config.MIN_QUESTION_PRICE,
            language=Language.get_for_request(self.request),
            country_id=country_id,
        )
        return kwargs


class UpdateQuestionValidationMixin(ValidationMixin):
    def validate(self):
        question = self.get_object()
        if question.status not in (QuestionStatus.DRAFT, QuestionStatus.DEFERRED):
            messages.error(self.request, _('You can not edit published question'))
            return redirect('answers:index', question_id=question.id, country_id=self.kwargs.get('country_id'))


class UpdateQuestionView(LoginRequiredMixin, UpdateQuestionValidationMixin, UpdateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'questions/edit.html'

    def get_success_url(self):
        return reverse('questions:my', kwargs={'country_id': self.kwargs.get('country_id')})


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


class QuestionsForStatusListView(QuestionsListView):
    status = None

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status=self.status)


class AnsweredQuestionsListView(QuestionsForStatusListView):
    status = QuestionStatus.ANSWERED


class PublishedQuestionsListView(QuestionsForStatusListView):
    status = QuestionStatus.PUBLISHED


class ClosedQuestionsListView(QuestionsForStatusListView):
    status = QuestionStatus.CLOSED


class MyQuestionsListView(MyListViewMixin, QuestionsListView):
    pass


class MyAnsweredQuestionsListView(MyListViewMixin, AnsweredQuestionsListView):
    pass


index = PublishedQuestionsListView.as_view()
create = CreateQuestionView.as_view()
edit = UpdateQuestionView.as_view()
closed = ClosedQuestionsListView.as_view()
answered = AnsweredQuestionsListView.as_view()
my = MyQuestionsListView.as_view()
my_answered = MyAnsweredQuestionsListView.as_view()
