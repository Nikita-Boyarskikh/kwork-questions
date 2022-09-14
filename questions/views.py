from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import ListView

from accounts.models import AccountAction, AccountActionType, AccountActionStatus
from languages.models import Language
from questions.forms import QuestionCreateForm
from questions.models import Question, QuestionStatus
from utils.translate import translate
from utils.views import CurrentCountryListViewMixin, MyListViewMixin


@transaction.atomic
def create(request, country_id):
    # TODO: split this common logic
    if not request.user.is_authenticated:
        messages.info(request, _('Only registered users can create questions.\nPlease, register.'))
        base_url = reverse(settings.LOGIN_URL)
        query_string = urlencode({'next': request.get_full_path_info()})
        return redirect(f'{base_url}?{query_string}')

    if not request.user.is_user_agreement_accepted:
        messages.info(request, _('You should accept site rules to create question.'))
        return redirect('rules:index')

    question = Question(
        author=request.user,
        price=settings.MIN_QUESTION_PRICE,
        language=Language.get_for_request(request),
        country_id=country_id,
    )
    form = QuestionCreateForm(instance=question)

    if request.method == 'POST':
        form = QuestionCreateForm(request.POST, instance=question)
        if form.is_valid():
            if 'translate' in request.POST:
                new_form_data = form.data.copy()
                new_form_data['en_text'] = translate(
                    text=form.cleaned_data['original_text'],
                    source_language=question.language,
                    target_language=Language.default,
                )
                form.data = new_form_data
            elif question.language == Language.default and not form.cleaned_data['en_text']:
                new_form_data = form.data.copy()
                new_form_data['en_text'] = form.cleaned_data['original_text']
                form.data = new_form_data
            elif not form.cleaned_data['en_text']:
                form.add_error('en_text', _('This field is required.'))
            else:
                question = form.save()
                return redirect(question)

    return render(request, 'questions/create.html', {
        'form': form,
    })


@login_required
def edit(request, country_id, pk):
    # TODO: repeat common validations
    question = Question.objects.get(pk=pk)
    if question.status not in (QuestionStatus.DRAFT, QuestionStatus.DEFERRED):
        messages.error(request, _('You can not edit published question'))
        return redirect('answers:index', question_id=pk, country_id=country_id)

    form = QuestionCreateForm(instance=question)

    if request.method == 'POST':
        form = QuestionCreateForm(request.POST, instance=question)
        if form.is_valid():
            if 'translate' in request.POST:
                new_form_data = form.data.copy()
                new_form_data['en_text'] = translate(
                    text=form.cleaned_data['original_text'],
                    source_language=question.language,
                    target_language=Language.default,
                )
                form.data = new_form_data
            elif question.language == Language.default and not form.cleaned_data['en_text']:
                new_form_data = form.data.copy()
                new_form_data['en_text'] = form.cleaned_data['original_text']
                form.data = new_form_data
            elif not form.cleaned_data['en_text']:
                form.add_error('en_text', _('This field is required.'))
            else:
                question = form.save()
                return redirect('questions:my', country_id=country_id)

    return render(request, 'questions/edit.html', {
        'form': form,
    })


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
closed = ClosedQuestionsListView.as_view()
answered = AnsweredQuestionsListView.as_view()
my = MyQuestionsListView.as_view()
my_answered = MyAnsweredQuestionsListView.as_view()
