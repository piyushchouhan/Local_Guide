from django import forms
from localguides.models import User, Guide, TrustedContact

class TrustedContactForm(forms.ModelForm):
    class Meta:
        model = TrustedContact
        fields = ['name', 'email', 'phone']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TrustedContactForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user
            self.fields['user'].widget = forms.HiddenInput()

