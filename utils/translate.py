from django.conf import settings

from google.api_core.exceptions import GoogleAPICallError
from google.cloud import translate_v2 as translate


translate_client = translate.Client()


class TranslationFailedError(Exception):
    pass


def translate(text, source_language, target_language):
    if source_language == target_language:
        return text

    try:
        result = translate_client.translate(
            text,
            target_language=target_language.google_id,
            source_language=source_language.google_id if source_language else None,
        )
    except GoogleAPICallError as e:
        raise TranslationFailedError(str(e))

    return result['translatedText']
