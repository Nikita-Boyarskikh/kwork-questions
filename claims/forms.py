from django import forms

from claims.models import Claim


class ClaimCreateForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ('comment',)
