from django import forms

from answers.models import Answer
from languages.models import Language
from translate.utils import translate


class AnswerCreateForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.en_text = translate(self.cleaned_data['original_text'], self.instance.language, Language.default)
        return super().save(commit)

    class Meta:
        model = Answer
        fields = ('original_text',)
