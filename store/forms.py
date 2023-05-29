from django import forms
from store.models import Contact
#

class FormContact(forms.ModelForm):
    name = forms.CharField(max_length=300, widget=forms.TextInput(attrs={
        'class': 'form-control fh5co_contact_text_box',
        'placeholder': 'Enter Your Name',
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control fh5co_contact_text_box',
        'placeholder': 'Email',
    }))
    phone_number = forms.CharField(max_length=400, widget=forms.TextInput(attrs={
        'class': 'form-control fh5co_contact_text_box',
        'placeholder': 'Phone',
    }))
    subject = forms.CharField(max_length=400, widget=forms.TextInput(attrs={
        'class': 'form-control fh5co_contact_text_box',
        'placeholder': 'Subject',
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control fh5co_contacts_message',
        'placeholder': 'Message',
    }))

    class Meta:
        model = Contact
        fields = '__all__'
        # fields = ('name', 'email', 'subject', 'message')
