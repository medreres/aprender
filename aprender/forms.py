from django import forms
from django.forms import TextInput, EmailInput, PasswordInput
from .models import Set, Folder, User
from django.forms import ModelForm


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
        'type':"email",
        'class':"form-control",
        'id':"emailInput",
        'placeholder':"Enter email"
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

# form for creating test


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
        fields = ('label', 'words', 'description', 'set_image')

    words = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'term_0',
    }))
    definitions = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'definition_0',
    }))

    # set_image = forms.ImageField(blank=True)

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
