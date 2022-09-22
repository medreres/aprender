from django import forms
from django.forms import TextInput, EmailInput, PasswordInput

class LoginForm(forms.Form):
   # username = forms.CharField(label='Username', max_length=100)
   username = forms.CharField(widget=forms.TextInput(attrs={
      'placeholder': 'email@example.com',
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