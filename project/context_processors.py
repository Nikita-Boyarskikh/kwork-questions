from django.db.models import Count
from django.urls import reverse
from django.utils.translation import gettext as _

from countries.models import Country
from languages.models import Language
from questions.models import QuestionStatus


def language(request):
    current_language = Language.get_for_request(request)
    return {
        'current_language': current_language,
        'languages': Language.objects.all(),
    }


def menu_items(request):
    country = Country.get_for_request(request)
    kwargs = {'country_id': country.id if country else 'unknown'}

    registered_items = [
        (reverse('users:me'), _('Avatar')),
        (reverse('questions:my', kwargs=kwargs), _('My questions')),
        (reverse('answers:my', kwargs=kwargs), _('My answers')),
        (reverse('questions:my_voting', kwargs=kwargs), _('My voting')),
        (reverse('likes:subscriptions', kwargs=kwargs), _('My Subscriptions')),
    ]

    not_admin_items = [
        (reverse('chat:index'), _('Chat')),
    ]

    return {
        'MENU_ITEMS': [
            (reverse('questions:create', kwargs=kwargs), _('Ask a question')),
            (reverse('rules:index'), _('Site rules')),
            *(registered_items if request.user.is_authenticated else []),
            *(not_admin_items if request.user.username != 'admin' else []),
            (reverse('questions:index', kwargs=kwargs), _('Opened questions')),
            (reverse('questions:voting', kwargs=kwargs), _('Voting')),
            (reverse('questions:closed', kwargs=kwargs), _('Closed questions')),
        ],
    }


def countries(request):
    return {
        'current_country': Country.get_for_request(request),
        'countries_with_questions': Country.objects
            .annotate(count=Count('question__id', distinct=True))
            .order_by('-count')
            .filter(question__status=QuestionStatus.PUBLISHED, count__gt=0).all(),
        'countries': Country.objects.all(),
    }
