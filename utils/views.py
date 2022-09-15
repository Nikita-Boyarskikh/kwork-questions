from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType


class CurrentCountryListViewMixin:
    country_field_name = 'country_id'

    def get_queryset(self):
        qs = super().get_queryset()
        country_id = self.kwargs.get('country_id')
        if country_id == 'None':
            return qs
        return qs.filter(**{self.country_field_name: country_id})


class MyListViewMixin(LoginRequiredMixin):
    owner_field_name = 'author'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(**{self.owner_field_name: self.request.user})


class ForGenericMixin:
    content_type_field = 'content_type'
    object_id_field = 'object_id'

    def get_queryset(self):
        qs = super().get_queryset()
        model_name = self.kwargs.get('content_type')
        content_type = ContentType.objects.filter(app_label=f'{model_name}s', model=model_name).first()
        return qs.filter(**{
            self.content_type_field: content_type,
            self.object_id_field: self.kwargs.get('object_id'),
        })


class ValidationMixin:
    def validate(self):
        pass

    def get(self, request, *args, **kwargs):
        response = self.validate()
        if response:
            return response
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = self.validate()
        if response:
            return response
        return super().post(request, *args, **kwargs)
