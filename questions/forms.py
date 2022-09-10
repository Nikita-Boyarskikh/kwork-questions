from django import forms

from questions.models import Question


class QuestionCreateForm(forms.ModelForm):
    en_text = forms.CharField(label=Question.en_text.field.verbose_name, widget=forms.Textarea, required=False)

    class Meta:
        model = Question
        fields = ('original_text', 'en_text', 'price')
