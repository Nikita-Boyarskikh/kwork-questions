from django import forms

from chat.models import Message


class CreateMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('')
