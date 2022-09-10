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
    country_id = request.resolver_match.kwargs.get('country_id') or request.session.get('country_id') or (
        request.user.country_id if request.user.is_authenticated else None
    )

    if country_id:
        request.session['country_id'] = country_id
    country_id_kwargs = {'country_id': country_id}

    registered_items = [
        (reverse('users:me'), _('Avatar')),
        (reverse('questions:my', kwargs=country_id_kwargs), _('My questions')),
        (reverse('answers:my', kwargs=country_id_kwargs), _('My answers')),
        (reverse('questions:my_voting', kwargs=country_id_kwargs), _('My voting')),
        (reverse('likes:subscriptions', kwargs=country_id_kwargs), _('My Subscriptions')),
    ]

    not_admin_items = [
        (reverse('chat:index'), _('Chat')),
    ]

    return {
        'MENU_ITEMS': [
            (reverse('questions:create', kwargs=country_id_kwargs), _('Ask a question')),
            (reverse('rules:index'), _('Site rules')),
            *(registered_items if request.user.is_authenticated else []),
            *(not_admin_items if request.user.username != 'admin' else []),
            (reverse('questions:index', kwargs=country_id_kwargs), _('Opened questions')),
            (reverse('questions:voting', kwargs=country_id_kwargs), _('Voting')),
            (reverse('questions:closed', kwargs=country_id_kwargs), _('Closed questions')),
        ],
    }


def countries(request):
    return {
        'countries_with_questions': Country.objects
            .annotate(count=Count('question__id', distinct=True))
            .order_by('-count')
            .filter(question__status=QuestionStatus.PUBLISHED, count__gt=0).all(),
        'countries': Country.objects.all(),
    }
