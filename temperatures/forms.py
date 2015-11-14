from django import forms
from .models import Newsletter


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Newsletter.objects.filter(email=email):
            raise forms.ValidationError('This email address is already in use.')
        return email
