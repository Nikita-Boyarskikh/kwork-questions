from functools import reduce

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.fields import AutoFieldMixin
from django.utils.functional import classproperty
from django.utils.module_loading import import_string

DefaultAutoField = import_string(settings.DEFAULT_AUTO_FIELD)
IntegerForAutoField = next(klass for klass in DefaultAutoField.__bases__ if klass is not AutoFieldMixin)


def content_type_limit_choices_by_model_references(model_references):
    def _reduce_model_references_to_content_type_query(query, model_reference):
        app_label, model = model_reference.split('.')
        criterion = models.Q(app_label=app_label.lower(), model=model.lower())
        return query | criterion
    return reduce(_reduce_model_references_to_content_type_query, model_references, models.Q())


class WithSelfContentTypeMixin:
    @classproperty
    def content_type(cls):
        return ContentType.objects.get_for_model(cls)
