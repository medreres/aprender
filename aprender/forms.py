from django import forms
from django.forms import TextInput, EmailInput, PasswordInput
from .models import Set, Folder


class LoginForm(forms.Form):
    # username = forms.CharField(label='Username', max_length=100)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'type': 'text',
        'class': 'form-control',
        'id': 'DropdownFormEmail1',
    }))
    # password = forms.CharField(label='Password',  max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'type': 'password',
        'class': 'form-control',
        'id': 'DropdownFormPassword1',
        'placeholder': 'Password',
    }))


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password',  max_length=100)
    password2 = forms.CharField(label='Password',  max_length=100)
    email = forms.CharField(label='Email',  max_length=100)


class CreateSet(forms.ModelForm):
   #  label = forms.CharField(label='Study Set Label', max_length=100)
    # ? Could be done better?
   #  term = forms.CharField(widget=forms.TextInput(attrs={
   #      'id': f"term_0",
   #  }))
   #  definition = forms.CharField(widget=forms.TextInput(attrs={
   #      'id': f"definition_0",
   #  }))

    class Meta:
        model = Set
        fields = ('label', 'words', 'description')

    words = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'term_0',
    }))
    definitions = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'definition_0',
    }))

    wordsList = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CreateFolder(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ('label', 'description')
    
    label = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-2',
        'type': 'text',
        'placeholder': 'Enter a title',
        'aria-label': 'Enter a title'
    }))

    description = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'type': 'text',
        'placeholder': 'Enter a description (optional)',
        'aria-label': 'Enter a description (optional)'
    }), required=False)
