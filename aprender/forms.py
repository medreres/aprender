from pydoc import describe
from django import forms
from django.forms import TextInput, EmailInput, PasswordInput
from .models import Set, Folder, User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


class EditUser(ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'email', 'profile_image')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',
        'id': 'usernameInput',
        'placeholder': 'Enter username'
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text",
        'class': "form-control",
        'id': "firstNameInput",
        'placeholder': "Enter First Name"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': "text",
        'class': "form-control",
        'id': "firstNameInput",
        'placeholder': "Enter First Name"
    }))

    email = forms.CharField(widget=forms.TextInput(attrs={
        'type': "email",
        'class': "form-control",
        'id': "emailInput",
        'placeholder': "Enter email"
    }))


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


class TestForm(forms.Form):
    QUESTION_TYPES = (
        ("written", "Written"),
        # ("matching", "Matching"),
        ("multiple", "Multiple Choices"),
        ("true", "True/False"),
    )
    STARRED_TERMS = (
        ('all', "All"),
        ('starred', 'Starred')
    )

    questionTypes = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={
            'name': "question",
            'type': "checkbox",
            'value': "written",
            'id': "written",
            'required': 'required'
        }), choices=QUESTION_TYPES)
    questionLimit = forms.IntegerField(widget=forms.NumberInput(attrs={
        # TODO
        'min': 5,
        'max': 35,
        'step': 5,
        'value': 5
    }))
    starredTerms = forms.ChoiceField(
        choices=STARRED_TERMS, widget=forms.RadioSelect(attrs={
            'class': "btn-check",
            'class': "btn-group",
            'role': "group",
        }), required=True)
    showImages = forms.BooleanField(label='Show Images', required=False)


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={
        # is-invalid TODO
        'class': "form-control ",
    }), required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'class': "form-control ",
    }))
    password_confirm = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput(attrs={
        'class': "form-control ",
    }))
    email = forms.CharField(label='Email',  max_length=100, widget=forms.TextInput(attrs={
        'class':"form-control ",
        'type': 'email'
    }))

    def clean(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password_confirm'):
            self.add_error('password_confirm', "Passwords do not match!")

        if len(User.objects.filter(username=cd.get('username'))) != 0:
            self.add_error(
                'username', "User with such username already exists!")
        return cd


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
        fields = ('label', 'words', 'description', 'set_image')

    label = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    description = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    words = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'term_0',
        'class': 'form-control',
        'placeholder': 'term'

    }))
    definitions = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'definition_0',
        'class': 'form-control',
        'placeholder': 'definition'
    }))

    # set_image = forms.ImageField(blank=True)



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
