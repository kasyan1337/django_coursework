from django import forms

from .models import Client, Message, Mailing


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'name', 'comment']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_time', 'period', 'status', 'message', 'clients', 'owner']
        widgets = {
            'clients': forms.CheckboxSelectMultiple(),
        }  # a widget that allows the user to select multiple clients from a list of checkboxes.
