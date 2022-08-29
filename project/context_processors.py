from django.db.models import Count
from django.urls import reverse
from django.utils.translation import gettext as _

from countries.models import Country
from languages.models import Language


def language(request):
    current_language = Language.get_for_request(request)
    return {
        'lang': current_language,
    }


def menu_items(request):
    country_id = request.session.get('country_id') or (
        request.user.country_id if request.user.is_authenticated else None
    ) or request.resolver_match.kwargs.get('country_id')

    if country_id:
        request.session['country_id'] = country_id
    country_id_kwargs = {'country_id': country_id}

    registered_items = [
        (reverse('users:me'), _('Avatar')),
        (reverse('chat:index'), _('Chat')),
        (reverse('questions:my', kwargs=country_id_kwargs), _('My questions')),
        (reverse('answers:my', kwargs=country_id_kwargs), _('My answers')),
        (reverse('questions:my_voting', kwargs=country_id_kwargs), _('My voting')),
        (reverse('likes:my', kwargs=country_id_kwargs), _('My Subscriptions')),
    ]

    return {
        'MENU_ITEMS': [
            (reverse('questions:create', kwargs=country_id_kwargs), _('Ask a question')),
            (reverse('rules:index'), _('Site rules')),
            *(registered_items if request.user.is_authenticated else []),
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
            .filter(count__gt=0).all(),
        'countries': Country.objects.all(),
    }
