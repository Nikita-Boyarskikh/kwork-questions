from django import forms
from django.conf import settings
from djmoney.money import Money

from languages.models import Language
from questions.models import Question
from translate.utils import translate


class QuestionCreateForm(forms.ModelForm):
    price__amount = forms.DecimalField(label=Question.price.field.verbose_name, min_value=0, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price__amount'].initial = kwargs.get('instance').price.amount

    def save(self, commit=True):
        price_amount = self.cleaned_data.pop('price__amount')
        self.instance.price = Money(price_amount, settings.DEFAULT_CURRENCY)
        self.instance.en_text = translate(self.cleaned_data['original_text'], self.instance.language, Language.default)
        self.instance.en_title = translate(self.cleaned_data['original_title'], self.instance.language, Language.default)
        return super().save(commit)

    class Meta:
        model = Question
        fields = ('original_title', 'original_text', 'price__amount')
