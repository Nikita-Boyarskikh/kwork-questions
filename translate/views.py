import json

from annoying.decorators import ajax_request
from django.views.decorators.http import require_POST

from languages.models import Language
from translate.utils import translate


@ajax_request
@require_POST
def translate_text(request):
    data = json.loads(request.body)
    text = data.get('text')
    source_language_id = data.get('source_language')
    source_language = Language.objects.get(id=source_language_id)
    return {'text': translate(text, source_language, target_language=Language.default)}
