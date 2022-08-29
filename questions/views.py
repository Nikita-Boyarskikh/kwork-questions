from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import ListView

from languages.models import Language
from questions.forms import QuestionCreateForm
from questions.models import Question, QuestionStatus
from questions.tasks import publish_question
from utils.translate import translate
from utils.views import CurrentCountryListViewMixin, MyListViewMixin


def create(request, country_id):
    if not request.user.is_authenticated:
        messages.info(request, _('Only registered users can create questions.\nPlease, register.'))
        base_url = reverse(settings.LOGIN_URL)
        query_string = urlencode({'next': request.get_full_path_info()})
        return redirect(f'{base_url}?{query_string}')

    question = Question(
        author=request.user,
        price=settings.MIN_QUESTION_PRICE,
        language=request.user.preferred_language,
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
                    source_language=form.cleaned_data['language'],
                    target_language=Language.default,
                )
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
def publish(request, country_id, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        messages.error(request, _('Question with this id does not exist'))
        return redirect('questions:index')

    task = publish_question.apply_async(kwargs={
        'question_id': request.POST.get('question_id'),
    }, countdown=60 * 60 * settings.PUBLISH_QUESTION_COUNTDOWN_HOURS)

    return redirect(question)


class QuestionsListView(ListView, CurrentCountryListViewMixin):
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
