from django import forms

from answers.models import Answer


class AnswerCreateForm(forms.ModelForm):
    en_text = forms.CharField(label=Answer.en_text.field.verbose_name, widget=forms.Textarea, required=False)

    class Meta:
        model = Answer
        fields = ('original_text', 'en_text')
