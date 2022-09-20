from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.views.generic import CreateView

from claims.models import Claim
from utils.views import ForGenericMixin, LoginRequiredMixin


class CreateClaimView(LoginRequiredMixin, ForGenericMixin, CreateView):
    model = Claim
    template_name = 'claims/create.html'
    fields = ('comment',)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        model_name = self.kwargs.get('content_type')
        content_type = ContentType.objects.filter(app_label=f'{model_name}s', model=model_name).first()
        kwargs['instance'] = Claim(
            author=self.request.user,
            object_id=self.kwargs.get('object_id'),
            content_type=content_type,
        )
        return kwargs

    def get_success_url(self):
        return self.object.claimed_object.get_absolute_url()

    def dispatch(self, request, *args, **kwargs):
        claim = self.get_queryset().first()
        if claim:
            return redirect(claim.claimed_object)


create = CreateClaimView.as_view()
