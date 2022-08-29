from django.contrib.auth.mixins import LoginRequiredMixin


class CurrentCountryListViewMixin:
    country_field_name = 'country_id'

    def get_queryset(self):
        qs = super().get_queryset()
        country = self.kwargs.get('country')
        if country is None:
            return qs
        return qs.filter(**{self.country_field_name: self.kwargs.get('country')})


class MyListViewMixin(LoginRequiredMixin):
    owner_field_name = 'author'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(**{self.owner_field_name: self.request.user})
