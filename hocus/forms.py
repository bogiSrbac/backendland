from django import forms
from .models import Defender

class CreateDefenderForm(forms.ModelForm):
    class Meta:
        model = Defender
        fields = ['nickname', 'tower']

    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        super(CreateDefenderForm, self).__init__(*args, **kwargs)
        self.fields['nickname'].widget.attrs['class'] = 'form-control'
        self.fields['tower'].widget.attrs['class'] = 'form-control'