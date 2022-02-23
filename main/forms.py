from django import forms
from .models import Nominee, Voter

class NomineeForm(forms.ModelForm):
    class Meta:
        model = Nominee

    def __init__(self, *args, **kwargs):
        super(NomineeForm, self).__init__(*args, **kwargs)