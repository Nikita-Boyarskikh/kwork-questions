from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import CreateView

from chat.forms import CreateMessageForm
from chat.models import Message
from users.models import User


class MessageListView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = CreateMessageForm
    template_name = 'chat/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['object_list'] = Message.objects.filter(
            Q(recipient=self.request.user) | Q(sender=self.request.user)
        ).all()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Message(
            sender=self.request.user,
            recipient=User.objects.get(username='admin'),
        )
        return kwargs

    def get(self, request, *args, **kwargs):
        request.user.inbox_messages.update(is_read=True)
        return super().get(request, *args, **kwargs)


index = MessageListView.as_view()
create = MessageListView.as_view()
