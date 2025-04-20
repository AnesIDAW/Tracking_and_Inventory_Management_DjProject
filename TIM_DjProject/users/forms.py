from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,  # Disable help text for username
            'email': None,     # Disable help text for email
            'password1': None, # Disable help text for password1
            'password2': None, # Disable help text for password2
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['password1', 'password2', 'username']:
            self.fields[field_name].help_text = ''